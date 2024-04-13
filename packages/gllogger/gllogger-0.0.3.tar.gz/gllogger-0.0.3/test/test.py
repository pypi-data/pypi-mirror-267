from gllogger import gL


class Test:
    def __init__(self):
        print("=========================")

        gL.infos("gL.infos")
        gL.warns("gL.warns")
        gL.errors("gL.errors")

        print("=========================")

        gL.getLogger(_n).infos("gL.getLogger(_n).infos")
        gL.getLogger(_n).warns("gL.getLogger(_n).warns")
        gL.getLogger(_n).errors("gL.getLogger(_n).errors")

        print("=========================")

        gL.getLogger(_n).debug("gL.getLogger(_n).debug")
        gL.getLogger(_n).info("gL.getLogger(_n).info")
        gL.getLogger(_n).warn("gL.getLogger(_n).warn")
        gL.getLogger(_n).warning("gL.getLogger(_n).warning")
        gL.getLogger(_n).error("gL.getLogger(_n).error")
        gL.getLogger(_n).exception("gL.getLogger(_n).exception")

        print("=========================")

    def test1(self):
        print("=========================")

        gL.infos("gL.infos")
        gL.warns("gL.warns")
        gL.errors("gL.errors")

        print("=========================")

        gL.getLogger(_n).infos("gL.getLogger(_n).infos")
        gL.getLogger(_n).warns("gL.getLogger(_n).warns")
        gL.getLogger(_n).errors("gL.getLogger(_n).errors")

        print("=========================")

        gL.getLogger(_n).debug("gL.getLogger(_n).debug")
        gL.getLogger(_n).info("gL.getLogger(_n).info")
        gL.getLogger(_n).warn("gL.getLogger(_n).warn")
        gL.getLogger(_n).warning("gL.getLogger(_n).warning")
        gL.getLogger(_n).error("gL.getLogger(_n).error")
        gL.getLogger(_n).exception("gL.getLogger(_n).exception")

        print("=========================")

    @classmethod
    def test2(cls):
        print("=========================")

        gL.infos("gL.infos")
        gL.warns("gL.warns")
        gL.errors("gL.errors")

        print("=========================")

        gL.getLogger(_n).infos("gL.getLogger(_n).infos")
        gL.getLogger(_n).warns("gL.getLogger(_n).warns")
        gL.getLogger(_n).errors("gL.getLogger(_n).errors")

        print("=========================")

        gL.getLogger(_n).debug("gL.getLogger(_n).debug")
        gL.getLogger(_n).info("gL.getLogger(_n).info")
        gL.getLogger(_n).warn("gL.getLogger(_n).warn")
        gL.getLogger(_n).warning("gL.getLogger(_n).warning")
        gL.getLogger(_n).error("gL.getLogger(_n).error")
        gL.getLogger(_n).exception("gL.getLogger(_n).exception")

        print("=========================")

    @staticmethod
    def test3():
        print("=========================")

        gL.infos("gL.infos")
        gL.warns("gL.warns")
        gL.errors("gL.errors")

        print("=========================")

        gL.getLogger(_n).infos("gL.getLogger(_n).infos")
        gL.getLogger(_n).warns("gL.getLogger(_n).warns")
        gL.getLogger(_n).errors("gL.getLogger(_n).errors")

        print("=========================")

        gL.getLogger(_n).debug("gL.getLogger(_n).debug")
        gL.getLogger(_n).info("gL.getLogger(_n).info")
        gL.getLogger(_n).warn("gL.getLogger(_n).warn")
        gL.getLogger(_n).warning("gL.getLogger(_n).warning")
        gL.getLogger(_n).error("gL.getLogger(_n).error")
        gL.getLogger(_n).exception("gL.getLogger(_n).exception")

        print("=========================")


def test():
    print("=========================")

    gL.infos("gL.infos")
    gL.warns("gL.warns")
    gL.errors("gL.errors")

    print("=========================")

    gL.getLogger(_n).infos("gL.getLogger(_n).infos")
    gL.getLogger(_n).warns("gL.getLogger(_n).warns")
    gL.getLogger(_n).errors("gL.getLogger(_n).errors")

    print("=========================")

    gL.getLogger(_n).debug("gL.getLogger(_n).debug")
    gL.getLogger(_n).info("gL.getLogger(_n).info")
    gL.getLogger(_n).warn("gL.getLogger(_n).warn")
    gL.getLogger(_n).warning("gL.getLogger(_n).warning")
    gL.getLogger(_n).error("gL.getLogger(_n).error")
    gL.getLogger(_n).exception("gL.getLogger(_n).exception")

    print("=========================")


if __name__ == "__main__":
    gL.setFunction(lambda text: print(text))
    gL.getLogger(__name__).init("function")

    print("=========================")

    gL.infos("gL.infos")
    gL.warns("gL.warns")
    gL.errors("gL.errors")

    print("=========================")

    _n = "gllogger.test"
    gL.getLogger(_n).infos("gL.getLogger(_n).infos")
    gL.getLogger(_n).warns("gL.getLogger(_n).warns")
    gL.getLogger(_n).errors("gL.getLogger(_n).errors")

    print("=========================")

    gL.getLogger(_n).debug("gL.getLogger(_n).debug")
    gL.getLogger(_n).info("gL.getLogger(_n).info")
    gL.getLogger(_n).warn("gL.getLogger(_n).warn")
    gL.getLogger(_n).warning("gL.getLogger(_n).warning")
    gL.getLogger(_n).error("gL.getLogger(_n).error")
    gL.getLogger(_n).exception("gL.getLogger(_n).exception")

    print("=========================")

    test()
    obj = Test()
    obj.test1()
    obj.test2()
    obj.test3()
