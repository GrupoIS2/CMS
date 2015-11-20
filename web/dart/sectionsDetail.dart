import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

//http://demo7492033.mockable.io/sections/#

class SectionResource {
    String path = "http://demo7492033.mockable.io/sections" + Uri.base.queryParameters['id'];
    List section_list;
    SectionResource(callback){
        HttpRequest.getString(path)
            .then((String fileSections) {
                this.section_list = JSON.decode(fileSections);
                print("Sections Loaded");
                callback();
            })
            .catchError((Error error) {
                print(error.toString());
            });
    }
}

var sectionResource ;

setContent(){
    querySelector('#id').value = sectionResource.section_list["id"];
    querySelector('#name').value = sectionResource.section_list["name"];
    querySelector('#description').value = sectionResource.section_list["description"];


}

void setSaveRequest(Event e)
{
    e.preventDefault();

    HttpRequest request = new HttpRequest();

    request.onReadyStateChange.listen((_) {
        if (request.readyState == HttpRequest.DONE && (request.status == 200 || request.status == 0)) 
        {
            window.alert("DONE");
        }
    });

    var url = "http://demo7492033.mockable.io/sections/1";
    request.open("POST", url, async: false);

    String jsonData = '{' + 
                            '"id": ' + querySelector("#id").value + ', ' +
                            '"name": ' + querySelector("#name").value + ', ' +
                            '"description": ' + querySelector("#description").value + ', ' +
                        '}';
    request.send(jsonData);
}

onSectionsReady(){
    setContent();
        querySelector("#form").onSubmit.listen(setSaveRequest);
}

void main() {
    sectionResource = new SectionResource(onSectionsReady);
}