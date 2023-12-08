
from configparser import ConfigParser

path = "config\database.ini"

def config_params(filename=path, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    parser.read(filename)
    
    # get section, default postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db