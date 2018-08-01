from .wwComponentBase import WWComponentBase


class WWSensorBase(WWComponentBase):

    def __init__(self, robot):
        super(WWSensorBase, self).__init__(robot)
        self._valid = False

    @property
    def valid(self):
        return self._valid

    def parse(self, single_component_dictionary):
        print("error: implement parse() for %s !" % (self.__class__.__name__))

    def __str__(self):
        return self.description()

    def description(self):
        if not self.valid:
            return "(not valid)"

        ret = ""
        delim = ''
        for fn in self._important_field_names():
            ret += "%s%s: %s" % (delim, fn, str(getattr(self, fn)))
            delim = ', '
        return ret

    def _important_field_names(self):
        return ()

    def _copy(self, other, include_none):
        field_names = ('_valid',) + self._important_field_names()
        self._copy_fields(other, field_names, include_none)

    def _copy_fields(self, other, field_name_list, include_none):
        for fn in field_name_list:
            if include_none or (getattr(other, fn) is not None):
                setattr(self, fn, getattr(other, fn))

    def _check_field_exists(self, single_component_dictionary, key):
        if key not in single_component_dictionary:
            err = "malformed sensor json. missing \"%s\"" % (key)
            raise ValueError(err)
        return True

    def check_fields_exist(self, single_component_dictionary, keys):
        ret = True
        for key in keys:
            ret = ret and self._check_field_exists(single_component_dictionary, key)
        return ret
