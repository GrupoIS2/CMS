import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

//http://demo7492033.mockable.io/sections

class SectionResource {
    String path = "http://demo7492033.mockable.io/sections";
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

    getSection(String name){
        for(var i=0;i<section_list.length; i++){
            if(section_list[i]["section_name"] == name){
                return section_list[i];
            }
        }
        return null;
    }
    getTable(){    
        TableElement table = new TableElement();
        table.classes.add("table");

        var tBody = table.createTBody();
        for(var i=0; i<section_list.length; i++){
            TableRowElement row = table.insertRow(i);

            TableCellElement cell = row.insertCell(-1);
            cell.text = section_list[i]["id"];

            cell = row.insertCell(-1);
            cell.text = section_list[i]["section_name"];

                cell = row.insertCell(-1);
            cell.text = section_list[i]["description"];
        }
        Element head = table.createTHead();
        TableRowElement headerRow =  table.tHead.insertRow(-1);
        var cell = new Element.tag('th');
        cell.text = 'id';
        headerRow.insertAdjacentElement('beforeend', cell);
        cell = new Element.tag('th');
        cell.text = 'section_name';
        headerRow.insertAdjacentElement('beforeend', cell);
        cell = new Element.tag('th');
        cell.text = 'description';
        headerRow.insertAdjacentElement('beforeend', cell);

    return table;
    }
}

setSection(){
    var table = sectionResource.getTable();
    querySelector('#table_list').append(table);
}

var sectionResource;

onSectionsReady(){
    setSection();
}


void main() {
    sectionResource = new SectionResource(onSectionsReady);
}

