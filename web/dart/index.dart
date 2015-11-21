import 'dart:html';
import 'dart:math' show Random;
import 'dart:convert' show JSON;
import 'dart:async' show Future;

class Admin {
    String info_url = "http://demo7492033.mockable.io/models/";
    List models;
    Admin(callback){
        HttpRequest.getString(info_url)
            .then((String url_content){
                this.models = JSON.decode(url_content);
                callback();
            })
            .catchError((Error error){
                print(error.toString());
            });
    }
    setAdminContent(){
        for(int i = 0; i<models.length; i++){
            var model = models[i];
            print('#model_' + (i+1).toString() + '_total_obj');
            querySelector('#model_' + (i+1).toString() + '_total_obj').text = model["total_objects"];
            querySelector('#model_' + (i+1).toString() + '_name').text = model["name"];
            //querySelector('#model_' + (i+1).toString() + '_url').href = model["url"] ;

        }
    }

}
var admin;

adminReady(){
    print(admin.info_url);
    print(admin.models);
    admin.setAdminContent();
}

main() {
    admin = new Admin(adminReady);
}
