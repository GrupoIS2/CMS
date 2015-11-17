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
    print("SAVE");
}

onSectionsReady(){
    setContent();
        querySelector("#form").onSubmit.listen(setSaveRequest);
}

void main() {
    sectionResource = new SectionResource(onSectionsReady);
}