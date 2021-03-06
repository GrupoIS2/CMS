import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

// http://demo8820132.mockable.io/contents/#

class ContentResource {
    String path = "http://demo8820132.mockable.io/contents/" + Uri.base.queryParameters['id'];
    List content_list;
    ContentResource(callback){
        HttpRequest.getString(path)
            .then((String fileContents) {
                this.content_list = JSON.decode(fileContents);
                print("Contents Loaded");
                callback();
            })
            .catchError((Error error) {
                print(error.toString());
            });
    }
}

var contentResource;

setContent(){
   querySelector('#id').value = contentResource.content_list["id"];
	 querySelector('#section').value = contentResource.content_list["section_name"];
   querySelector('#title').value = contentResource.content_list["title"];
	 querySelector('#body').value = contentResource.content_list["body"];
	 querySelector('#user_name').innerHtml = contentResource.content_list["user_name"];
	 querySelector('#user_name').href = contentResource.content_list["user"];
   querySelector('#created').innerHtml = contentResource.content_list["created"];
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
	var url = "http://demo7492033.mockable.io/contents/1";
	request.open("POST", url, async: false);

	String jsonData = '{' + 
										'"id": ' + querySelector("#id").value + ', ' +
										'"title": "' + querySelector("#title").value + '", ' +
										'"body": "' + querySelector("#body").value + '", ' +
										'"section_name": "' + querySelector("#section").value + '"' +
										'}';
	request.send(jsonData);
}

onContentsReady(){
    setContent();
		querySelector("#form").onSubmit.listen(setSaveRequest);
}

void main() {
    contentResource = new ContentResource(onContentsReady);
}
