from os.path import dirname, abspath, join

file_name = 'url_list.json'
skill_path = "/opt/mycroft/skills/skill-url-radio.pcwii"
with open(join(skill_path, file_name)) as f:
    self.channel_list = json.load(f)
self.log.info(str(self.channel_list))
