import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/xdkazer/Dual_Kuka_LLM_Bachelor/p5_ws/install/moveit_configs_utils'
