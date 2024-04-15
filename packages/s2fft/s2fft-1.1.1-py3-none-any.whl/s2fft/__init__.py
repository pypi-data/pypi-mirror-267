from . import logs
from .transforms import wigner
from .transforms.spherical import *
from .recursions.price_mcewen import (
    generate_precomputes,
    generate_precomputes_jax,
    generate_precomputes_wigner,
    generate_precomputes_wigner_jax,
)
from .utils.rotation import rotate_flms, generate_rotate_dls

import logging
import jax

if jax.config.read("jax_enable_x64") is False:
    logger = logging.getLogger("s2fft")
    logger.warning(
        "JAX is not using 64-bit precision. This will dramatically affect numerical precision at even moderate L."
    )
