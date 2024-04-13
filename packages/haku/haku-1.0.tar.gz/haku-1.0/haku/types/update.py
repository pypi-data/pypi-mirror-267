#HALO INI ADALAH CLONE DARI PYROFORK.

import haku


class Update:
    @staticmethod
    def stop_propagation():
        raise haku.StopPropagation

    @staticmethod
    def continue_propagation():
        raise haku.ContinuePropagation
