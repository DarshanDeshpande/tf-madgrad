"""Madgrad optimizer implementation."""

from tensorflow.python.framework import ops
from tensorflow.python.keras import backend_config
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import cond_v2
from tensorflow.python.util.tf_export import keras_export


@keras_export("keras.optimizers.MadGrad")
class MadGrad(optimizer_v2.OptimizerV2):
    r"""Optimizer that implements the MADGRAD algorithm.

    Args:
      learning_rate: A Tensor or a floating point value.  The learning rate.
      momentum: A float value or a constant float tensor. Accelerates in the
      direction of gradient descent and dampens oscillations
      weight_decay: A float value or a constant float tensor. Factor by which
      the weights are decayed
      epsilon: A small constant for numerical stability.
      name: Optional name for the operations created when applying gradients.
        Defaults to `"Madgrad"`.
      **kwargs: Keyword arguments. Allowed to be one of
        `"clipnorm"` or `"clipvalue"`.
        `"clipnorm"` (float) clips gradients by norm; `"clipvalue"` (float) clips
        gradients by value.

    Usage Example:
      # >>> opt = MadGrad(learning_rate=0.2)
      # >>> var1 = tf.Variable(10.0)
      # >>> loss = lambda: (var1 ** 2) / 2.0
      # >>> step_count = opt.minimize(loss, [var1]).numpy()
      # >>> "{:.1f}".format(var1.numpy())
      9.3

    Reference:
      - [Aaron Defazio and Samy Jelassi, 2021](https://arxiv.org/abs/2101.11075).
    """

    _HAS_AGGREGATE_GRAD = True

    def __init__(
        self,
        learning_rate=0.01,
        momentum=0.9,
        weight_decay=0,
        epsilon=1e-6,
        name="Madgrad",
        **kwargs
    ):
        learning_rate = kwargs.get("lr", learning_rate)
        super(MadGrad, self).__init__(name, **kwargs)
        self._set_hyper("learning_rate", kwargs.get("lr", learning_rate))
        self._set_hyper("decay", self._initial_decay)
        self._set_hyper("momentum", momentum)
        self._set_hyper("weight_decay", weight_decay)
        self.epsilon = epsilon or backend_config.epsilon()
        self._first_step = True

    def _create_slots(self, var_list):
        for var in var_list:
            self.add_slot(var, "vk")
        for var in var_list:
            self.add_slot(var, "sk")
        for var in var_list:
            self.add_slot(var, "x_0")

    def _prepare_local(self, var_device, var_dtype, apply_state):
        momentum = array_ops.identity(self._get_hyper("momentum", var_dtype))
        weight_decay = array_ops.identity(self._get_hyper("weight_decay", var_dtype))

        apply_state[(var_device, var_dtype)] = dict(
            epsilon=ops.convert_to_tensor_v2(self.epsilon, var_dtype),
            momentum=momentum,
            weight_decay=weight_decay,
        )

    def _resource_apply_dense(self, grad, var, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get(
            (var_device, var_dtype)
        ) or self._fallback_apply_state(var_device, var_dtype)

        vk = self.get_slot(var, "vk")
        sk = self.get_slot(var, "sk")
        x_0 = self.get_slot(var, "x_0")

        decay = math_ops.cast(self._get_hyper("weight_decay"), var_dtype)
        lr_t = self._decayed_lr(var_dtype)

        grad = cond_v2.cond_v2(
            math_ops.greater(decay, 0),
            lambda: grad + decay * var,
            lambda: grad,
        )

        local_step = math_ops.cast(self.iterations + 1, var_dtype)
        lamb = lr_t * math_ops.pow(local_step, 0.5)
        if self._first_step:
            x_0 = state_ops.assign(x_0, var, use_locking=self._use_locking)
            self._first_step = False

        sk_plus_1 = state_ops.assign_add(sk, lamb * grad, use_locking=self._use_locking)
        vk_plus_1 = state_ops.assign_add(
            vk, lamb * (grad * grad), use_locking=self._use_locking
        )

        z_k_plus_1 = (
            x_0
            - (1 / (math_ops.pow(vk_plus_1, (1.0 / 3.0)) + coefficients["epsilon"]))
            * sk_plus_1
        )

        var_t = (1 - coefficients["momentum"]) * var + (
            coefficients["momentum"] * z_k_plus_1
        )

        return state_ops.assign(var, var_t, use_locking=self._use_locking).op

    def _resource_apply_sparse(self, grad, var, indices, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get(
            (var_device, var_dtype)
        ) or self._fallback_apply_state(var_device, var_dtype)

        vk = self.get_slot(var, "vk")
        sk = self.get_slot(var, "sk")
        x_0 = self.get_slot(var, "x_0")

        decay = math_ops.cast(self._get_hyper("weight_decay"), var_dtype)
        lr_t = self._decayed_lr(var_dtype)

        grad = cond_v2.cond_v2(
            math_ops.greater(decay, 0),
            lambda: grad + decay * array_ops.gather(var, indices),
            lambda: grad,
        )
        local_step = math_ops.cast(self.iterations + 1, var_dtype)

        lamb = lr_t * math_ops.pow(local_step, 0.5)

        if self._first_step:
            x_0 = state_ops.assign(x_0, var, use_locking=self._use_locking)
            self._first_step = False

        sk_plus_1 = self._resource_scatter_add(sk, indices, lamb * grad)
        vk_plus_1 = self._resource_scatter_add(vk, indices, lamb * (grad * grad))

        z_k_plus_1 = (
            x_0
            - (1 / (math_ops.pow(vk_plus_1, (1.0 / 3.0)) + coefficients["epsilon"]))
            * sk_plus_1
        )

        var_t = (1 - coefficients["momentum"]) * var + (
            coefficients["momentum"] * z_k_plus_1
        )
        return state_ops.assign(var, var_t, use_locking=self._use_locking).op

    def get_config(self):
        config = super(MadGrad, self).get_config()
        config.update(
            {
                "learning_rate": self._serialize_hyperparameter("learning_rate"),
                "momentum": self._serialize_hyperparameter("momentum"),
                "weight_decay": self._serialize_hyperparameter("weight_decay"),
                "epsilon": self.epsilon,
            }
        )
        return config
