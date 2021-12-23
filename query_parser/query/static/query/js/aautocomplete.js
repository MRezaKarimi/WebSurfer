var matches = [];

$('#search_input').keyup(function (){
    console.clear()
    var input_val = $(this).val();
    var l = input_val.split(' ');
    var x = l[l.length - 1];
    if(x !== ""){
        re = RegExp('^'+x)
        matches = words.filter(i => re.test(i)).slice(0,20);
        console.log(matches)
        $('#autocomplete').empty()
        for(i of matches){
            $('#autocomplete').append('<option value="' + l.slice(0, l.length - 1).join(' ') + ' ' + i + '">')
        }
        // $( "#search_input" ).autocomplete({
        //     delay: 00,
        //     minLength: 1,
        //     source: matches
        // });
    }
});

