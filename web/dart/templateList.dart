import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;


class TemplateList{

    var request_url = "http://demo3747392.mockable.io/template_model";
    List json_template_list;
    TemplateList(callback){
        HttpRequest.getString(request_url)
            .then((String fileContents) {
                this.json_template_list = JSON.decode(fileContents);
                print(this.json_template_list);
                callback();
                
            })
            .catchError((Error error) {
                print(error.toString());
            });
    }
}

var templateList;

fillTable(){
    var table = query(".table");
    for (var i=0; i<templateList.json_template_list.length; i++){
        TableRowElement row = table.insertRow(-1);
        row.insertCell(0).text = templateList.json_template_list[i]['id'];
        row.insertCell(1).text = templateList.json_template_list[i]['name_template'];
        row.insertCell(2).text = templateList.json_template_list[i]['default_use'];
        row.insertCell(3).text = templateList.json_template_list[i]['resource'];
        row.insertCell(4).text = templateList.json_template_list[i]['description'];
            
    }
    
}

void main() {

    templateList = new TemplateList(fillTable);

}
