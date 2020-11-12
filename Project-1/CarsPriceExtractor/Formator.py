import json


class FormatResults:

    results_file_name = None

    def __int__(self):
        pass

    def create_json_file(self, data):

        data = json.dumps(data, indent=4)

        with open(self.results_file_name + '.json', "w") as f:
            f.write(data)

    def create_html_file(self):

        html_code = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{self.results_file_name}</title>
        <link rel="icon" href="https://i.ibb.co/ZKbJ5L4/logo-removebg-preview.png" type="image/icon type">
    </head>
    <body>
        
        <h2 id= "res-title"></h2>
        <center><img src="https://i.ibb.co/ZKbJ5L4/logo-removebg-preview.png"></center>
        <script type="text/javascript" src="{self.results_file_name}.js"></script>
    </body>
</html>
"""
        with open(self.results_file_name + ".html", "w") as f:
            f.write(html_code)

    def create_js_file(self, data):

        js_code = """
resTitle = document.getElementById("res-title");
resTitle.innerHTML = '""" + self.results_file_name + """ Results'
resTitle.setAttribute("align", "center");

function createCarLink(CAR) {
    var h3Tag = document.createElement("h3");
    var linkTag = document.createElement("a");
    linkTag.innerText = CAR.name;
    linkTag.setAttribute('href', CAR.link);
    h3Tag.innerHTML = '<a href="' + CAR.link + '">' + CAR.name + '</a> Price: ' + CAR.price;
    document.body.appendChild(h3Tag);
}

for (car of data) {
    createCarLink(car);
}
        """
        line_to_append = "var data = ["

        self.create_json_file(data)

        with open(self.results_file_name + ".json") as f:
            lines = f.readlines()

        lines[0] = line_to_append
        lines.append(js_code)

        with open(self.results_file_name + ".js", "w") as f:
            f.writelines(lines)

    def create_html_js_result_file(self, data):

        self.create_html_file()
        self.create_js_file(data)
