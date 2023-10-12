
class JobAd:

    def __init__(self, info, update_date, content):
        self.info = self.prep_info(info)
        self.update_date = update_date
        self.content = content
        self.info.append(self.content)
        self.info.append(self.update_date)

    # get methods
    def get_info(self):
        return self.info

    def get_update_date(self):
        return self.update_date

    def get_content(self):
        return self.content

    def prep_info(self, info):
        for i in range(len(info)):
            info[i] = info[i].text
        info.remove(info[0])
        for element in info:
            info = element.split('\"')
        info = info[1:-1]
        for i in info:
            if i == ': ' or i.__contains__('\n          '):
                info.remove(i)
        for j in info:
            if j.__contains__("CV") or j.__contains__("post_ListingStatus"):
                info.remove(j)
        return info
