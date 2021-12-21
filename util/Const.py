class Const():
    class ConstError(TypeError):
        pass
    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            raise self.ConstError(f"Can't change a const variable {key}")
        self.__dict__[key] = value

    def __delattr__(self, key):
        if key in self.__dict__.keys():
            raise self.ConstError(f"Can't delete a const variable {key}")

        raise AttributeError(f"Isn't exist const variable {key}")