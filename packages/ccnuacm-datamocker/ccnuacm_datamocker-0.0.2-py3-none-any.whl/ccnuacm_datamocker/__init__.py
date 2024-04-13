__all__ = ["set_seed", "set_work_dir"]
__author__ = "JixiangXiong"


def set_seed(seed_):
    from .common import context
    context().random.set_seed(seed_)
    context().logger.info(f"Setting random seed to `{seed_}`")


def set_work_dir(work_dir):
    from .common import context
    context().work_dir = work_dir


def set_compiler(compiler_path):
    from .common import context
    context().CXX = compiler_path
    context().logger.info(f"Setting compiler path to `{compiler_path}`")
