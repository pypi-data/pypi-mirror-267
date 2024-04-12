class University:
    def __init__(self, uid, cn_name, en_name, code, authority, location, level, note = None):
        '''
        :param uid: Just random id, classified by prefecture-level cities
        :param cn_name: Cn_university_name
        :param en_name: Translated en_university_name
        :param code: Grant number
        :param authority: Competent authority
        :param location: Location
        :param level: School level
        :param note: note
        '''
        self.uid = uid
        self.cn_name = cn_name
        self.en_name = en_name
        self.code = code
        self.authority = authority
        self.location = location
        self.level = level
        self.note = note

    def __repr__(self):
        return f'University({self.uid}, "{self.cn_name}", "{self.en_name}", "{self.code}", "{self.authority}", "{self.location}", "{self.level}", "{self.note}")'