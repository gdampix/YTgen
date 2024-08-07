from bs4 import BeautifulSoup



class SlideParser:

    def __init__(self, template_path) -> None:
        with open(template_path, "r") as f:
            self.template_string = f.read()


    def parse_template(self, data=dict(), correct_target=None):
        if not len(data):
            print("no data to parse template.")
            return self.template_string
        
        # Load the HTML string into BeautifulSoup
        soup = BeautifulSoup(self.template_string, 'html.parser')

        for key, val in data.items():
            element = soup.find(id=key)
            if element:
                element.string = val

        if correct_target:
            soup.find(id=correct_target)['class']='option_correct'
        
        return soup.prettify()


if __name__=="__main__":
    parser = SlideParser("slide_template.html")
    parsed_html = parser.parse_template(
        {"id_question":"id_question",
        "id_option_1":"id_option_1",
        "id_option_2":"id_option_2",
        "id_option_3":"id_option_3",
        "id_option_4":"id_option_4",
        },
        "id_option_3")
    
    print(parsed_html)

