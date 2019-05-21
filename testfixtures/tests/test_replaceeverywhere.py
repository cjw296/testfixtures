from testfixtures.replace import ReplaceEverywhere

target = object()


def target_id():
    return id(target)


class TestSingleReplace(object):

    def test_in_globals(self):
        target_id_ = target_id()
        replacement = object()
        replacement_id = id(replacement)

        with ReplaceEverywhere(target, replacement):

            assert target_id() == replacement_id

        assert target_id() == target_id_

    def test_in_locals(self):
        target = object()
        target_id = id(target)
        replacement = object()
        replacement_id = id(replacement)

        with ReplaceEverywhere(target, replacement):

            assert id(target) == replacement_id

        assert id(target) == target_id_
