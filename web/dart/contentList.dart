import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

// http://demo8820132.mockable.io/contents

class ContentResource {
    String path = "http://demo8820132.mockable.io/contents";
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

    getContent(String name){
        for(var i=0;i<content_list.length; i++){
            if(content_list[i]["content_name"] == name){
                return content_list[i];
            }
        }
        return null;
    }   

    getTable(){	
	TableElement table = new TableElement();
	table.classes.add("table");

	var tBody = table.createTBody();
	for(var i=0; i<content_list.length; i++){
	    TableRowElement row = table.insertRow(i);

	    TableCellElement cell = row.insertCell(-1);
	    cell.text = content_list[i]["id"];

	    cell = row.insertCell(-1);
	    cell.text = content_list[i]["title"];

            cell = row.insertCell(-1);
	    cell.text = content_list[i]["body"];

            cell = row.insertCell(-1);
	    cell.text = content_list[i]["created"];

            cell = row.insertCell(-1);
	    cell.text = content_list[i]["section_name"];
	    
            cell = row.insertCell(-1);
	    cell.text = content_list[i]["user_name"];


	    cell = row.insertCell(-1);
	    cell.text = content_list[i]["section"];

            cell = row.insertCell(-1);
	    cell.text = content_list[i]["user"];
   	}

	Element head = table.createTHead();
	TableRowElement headerRow =  table.tHead.insertRow(-1);
	var cell = new Element.tag('th');
	cell.text = 'id';
	headerRow.insertAdjacentElement('beforeend', cell);

	cell = new Element.tag('th');
	cell.text = 'title';
	headerRow.insertAdjacentElement('beforeend', cell);

	cell = new Element.tag('th');
	cell.text = 'body';
	headerRow.insertAdjacentElement('beforeend', cell);
        
	cell = new Element.tag('th');
	cell.text = 'created';
	headerRow.insertAdjacentElement('beforeend', cell);

	cell = new Element.tag('th');
	cell.text = 'section_name';
	headerRow.insertAdjacentElement('beforeend', cell);
	
	cell = new Element.tag('th');
	cell.text = 'user_name';
	headerRow.insertAdjacentElement('beforeend', cell);
        
	cell = new Element.tag('th');
	cell.text = 'section';
	headerRow.insertAdjacentElement('beforeend', cell);


	cell = new Element.tag('th');
	cell.text = 'user';
	headerRow.insertAdjacentElement('beforeend', cell);

	return table;
    }
}

setContent(){
   var table = contentResource.getTable();
   querySelector('#table_list').append(table);
}

var contentResource;

onContentsReady(){
    setContent();
}

void main() {
    contentResource = new ContentResource(onContentsReady);
}
