
function translate_text(text_dict){
    var lang = document.documentElement.lang.toLowerCase();

    if(text_dict[lang] !== undefined)
        return text_dict[lang];
    return text_dict['en'];
}