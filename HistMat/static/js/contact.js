 
var contact_def =  {
    name : "",
    surname : "",
    email : "",
    phone : "",
    direction : "",
    marle : false,
    luxem : false
}
console.log("Iniciando");
var contact_app = new Vue({
    el: '#contact-app',
    delimiters: ['[[', ']]'],
    data : {
        contact : {},
        contact_list : [],
        errors : []
    },
    created : function() {
        console.log("Creando");
        this.contact= {...contact_def};
        console.log("Leyendo");
        db.collection("contactos").get().then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
                this.contact_list.push(doc.data());
                console.log(`Agregando el elemento ${doc.id} => ${doc.data().name}`);
            });
        });
    },
    methods : {
        add_contact(){
            this.errors = [];
            if(this.contact.name.length == 0 || this.contact.name.length > 31)
                this.errors.push("Name must be between 1 and 31 characters");
            
            if(!this.contact.phone)
                this.errors.push("The phone number is compulsory");
            
            if(!/\S+@\S+\.\S+/.test(this.contact.email))
                this.errors.push("The email is invalid");

            if(this.errors.length>0)
                return;

            this.contact_list.push({...this.contact});
            
            db.collection("contactos").add(this.contact)
            .then(function(docRef) {
                console.log("Document written with ID: ", docRef.id);
            })
            .catch(function(error) {
                console.error("Error adding document: ", error);
            });

            this.contact= {...contact_def};
        },
    }
    
});