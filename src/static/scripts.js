

$(function() {

    $.getJSON( 'https://api.coinmarketcap.com/v1/ticker/', function( data ) {
      var names = [];
      var all = [];
      $.each( data, function( key, val ) {
            names.push( val['name'] );
            all.push([val['name'], val['price_usd'], val['price_btc'], val['symbol']]);
        });
      console.log(names);
        $('#crypto_chooser input').autocomplete({
          source: names
            });

        $('#crypto_chooser input').on('change keydown focusout click', function(e){
            var crypto_name = $(this).val();
            console.log(crypto_name);
            console.log(names.indexOf(crypto_name));
            var position =  names.indexOf($(this).val());
            var btc_value = parseFloat(all[position][2]);
            var usd_value = parseFloat(all[position][1]);
            var eth_value = (parseFloat(all[position][2]) / all[names.indexOf('Ethereum')][2]).toFixed(5)

            $('#chosen_icon').removeClass().addClass('cc ' + all[position][3]);

            $('#btc_value').text(btc_value);
            $('#eth_value').text(eth_value);
            $('#usd_value').text('$' + usd_value);

        });
    });

     $("[name='user_email']").blur(function() {
        var email = this.value;
        var sms = $("[name='user_phone']").val();
        email_and_sms_validator(email, sms);
     });

      $("[name='user_phone']").blur(function() {
        var sms = this.value;
        var email = $("[name='user_email']").val();
        email_and_sms_validator(email, sms);
     });


    $('#crypto-alert-create').click(function() {
        var form_data = $('form').serializeArray()
        var coin_current_price = parseFloat($('#btc_value').text());
        var coin_alert_price = parseFloat($("[name='amount_chooser']").val());

        form_data.push({'name': 'btc_price_at_creation', 'value': coin_current_price})

        console.log(form_data);
            $.ajax({
                url: '/crypto_form_consumer',
                data: $.param(form_data),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
            
        alert_message();


        });


// $('last_submit_message').text(alert_message());

});

function alert_message(){
    var form_data = {}
    $('form').serializeArray().map(function(x){form_data[x.name] = x.value;}); 
    var delivery_methods = "";
    var direction = "";
    var message = "";
    // convert delivery methods into a string
    if (form_data['user_email'] && form_data['user_email']){
        delivery_methods = "SMS and Email alerts";
    } else if (form_data['user_email']) {
        delivery_methods = 'an email alert to ' + form_data['user_email'];
    } else {
        delivery_methods = 'an SMS alert to' + form_data['user_phone'];
    }
    
    if (form_data['amount_chooser'] < form_data['btc_price_at_creation']) {
        direction = "dropped below ";
    } else {
        direction = "risen above ";
    }
    
    message = 'New '+ form_data['crypto_chooser'] + ' alert created: You will receive ' +
    delivery_methods + ' when ' + form_data['crypto_chooser'] + ' has ' + direction +
    form_data['amount_chooser'];
    console.log(message);
    $('#last_submit_message').text(message);
    return message;
}

function email_and_sms_validator(email, sms){
    var regex_email = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var regex_sms = /^\s*(?:\+?(\d{1,3}))?[- (]*(\d{3})[- )]*(\d{3})[- ]*(\d{4})(?: *[x/#]{1}(\d+))?\s*$/;

    var email_test = regex_email.test(email);
    var sms_test = regex_sms.test(sms)

    var currency = $('#crypto_chooser input').val();

    if (email_test && sms_test) {
            $('#crypto-alert-create').text('Create both SMS and EMAIL alerts for ' + currency)
        } else if (email_test && !sms_test) {
            $('#crypto-alert-create').text('Create an EMAIL alert for ' + currency)
        } else if (sms_test && !email_test) {
            $('#crypto-alert-create').text('Create an SMS alert for ' + currency)
        }else {
            $('#crypto-alert-create').text('Please enter a delivery method to create an alert!')
        };
}