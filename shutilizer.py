import shutil

class Shutilizer:


    @staticmethod
    def copytree_to_dst(src, dst, ignore=None, **kwargs):
        try:
            shutil.copytree(src, dst, ignore)
        except Exception as e:
            return e