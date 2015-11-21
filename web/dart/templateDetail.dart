import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

// http://demo8820132.mockable.io/contents/#

class ContentResource {
    String path = "http://demo3747392.mockable.io/template_detail";
    List content_list;
    ContentResource(callback){
        HttpRequest.getString(path)
            .then((String fileContents) {
                this.content_list = JSON.decode(fileContents);
                print(this.content_list);
                callback();
            })
            .catchError((Error error) {
                print(error.toString());
            });
    }
}

var contentResource;

setContent(){
   querySelector('#name').value = contentResource.content_list["name_template"];
   querySelector('#default').value = contentResource.content_list["default_use"];
   querySelector('#resource').value = contentResource.content_list["resource"];
   querySelector('#description').value = contentResource.content_list["description"];
   
}

void setSaveRequest(Event e)
{
  e.preventDefault();

    HttpRequest request = new HttpRequest();

    request.onReadyStateChange.listen((_) {
        if (request.readyState == HttpRequest.DONE && 
                (request.status == 200 || request.status == 0)) {
        window.alert("Section saved.");
        }
    });

    // POST the data to the server
    var url = "http://demo3747392.mockable.io/save_template";
    request.open("POST", url, async: false);
    var mapData = new Map();

    mapData['id'] = contentResource.content_list['id'];
    mapData['name_template'] = querySelector("#name").value;
    mapData['default_use'] = querySelector("#default").value;
    mapData['resource'] = querySelector("#resource").value;
    mapData['description'] = querySelector("#description").value;
    String jsonData = JSON.encode(mapData);
    request.send(jsonData);
}

onContentsReady(){
    setContent();
        querySelector("#form").onSubmit.listen(setSaveRequest);
}

void main() {
    contentResource = new ContentResource(onContentsReady);
}
