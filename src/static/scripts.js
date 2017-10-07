$(function() {


    // Currency choice buttons and currency icon changer
    $('#currency_choice button').click(function() {
        var currency_choice = $(this)
        currency_choice_and_icons(currency_choice)
    });

    $('#crypto_chooser').focusin(function(){
        $('#helper-text').slideUp();
    })
    
    // Get altcoin ticker from coinmarketcap
    $.getJSON('https://api.coinmarketcap.com/v1/ticker/', function(data) {
        var names = [];
        var all = [];
        $.each(data, function(key, val) {
            names.push(val['name']);
            all.push([val['name'], val['price_usd'], val['price_btc'], val['symbol']]);
        });

        $('#crypto_chooser').autocomplete({
            source: names,
            minlength: 0,
            change: function(event) {
                var coin = $(this).val();
                if (coin === null || ($.inArray(coin, names) == -1)) {
                    $(this).val(''); /* clear the value */
                    $(this).attr('placeholder', 'Please choose a coin from the dropdown');
                } else {
                    crypto_chooser_success(coin, names, all);
                    $('#conversion_amounts').slideDown();
                }
            }
        });
    });

    // Submit form data
    $('#crypto-alert-create').click(function() {
        // Validate coin and currency boxes not empty
        if (!coin_and_currency_validaion()) { return; }

        // Validate email and/or SMS
        var email_and_sms = email_and_sms_validator()
        if (!email_and_sms['email'] && !email_and_sms['sms']) {
            return;
        }

        // Get all form data: Coin, Alert Price, Email, and SMS
        var form_data = $('form').serializeArray()

        // // Data not captured in the form
        var alert_currency = $('button.currency_choice').text();
        var coin_current_price = parseFloat($('td.coin_current_price').attr('data-value'));

        // Add some data to the form
        form_data.push({ 'name': 'coin_current_price', 'value': coin_current_price })
        form_data.push({ 'name': 'alert_currency', 'value': alert_currency })
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
        
        // Display last submitted alert info box
        var succesful_alert_message = alert_created_message();
        console.log(succesful_alert_message);
        
        $('#helper-text').slideDown().text(succesful_alert_message);

        // Reset all form fields
        document.getElementById('form').reset();
        // Reset conversion boxes
        $('.currency_conversion_foreground').text('');

        // end submit form data
    });

    // Site owner social links
    $('#email-container').hover(function() {
        $('#email').show();
    });

    $('#email').parent('li').mouseleave(function() {
        $('#email').toggle();
    });

    $('[name="email"]').focusout(function() {
        email_and_sms_validator()
    });
    
    $('#alert_price').blur(function(){
            pre_submit_help_alert()
        });
});

function pre_submit_help_alert() {
    
    var alert_coin = $('#crypto_chooser').val();
    var coin_current_price = parseFloat($('.coin_current_price').attr('data-value'));
    var alert_currency = $('.currency_choice').text();
    var alert_price = $('[name="alert_price"]').val();
    var message = ''
    
    console.log(alert_coin, coin_current_price, alert_currency, alert_price)
    
    // Establish if the alert is for a higher price or a lower price
    if (alert_coin && alert_price && coin_current_price && alert_currency) {
        $('#helper-text').slideDown();
        if (parseFloat(coin_current_price) > parseFloat(alert_price)) {
            message = 'You are creating a one-time for alert when ' + alert_coin + ' falls below ' + alert_price + alert_currency;
        }
        else {
            message = 'You are creating a one-time for alert when ' + alert_coin + ' rises above ' + alert_price + alert_currency;
        }
    $('#helper-text').text(message)
};
    // Update the alert message with the right contact data
    // if (email && sms) {
    //     $('#crypto-alert-create').text('Send me both SMS and EMAIL alerts for ' + currency + direction)
    //     return true;
    // }
    // else if (email && !sms) {
    //     $('#crypto-alert-create').text('Send me an EMAIL alert for ' + currency + direction)
    //     return true;
    // }
    // else if (sms && !email) {
    //     $('#crypto-alert-create').text('Send me an SMS alert for ' + currency + direction)
    //     return true;
    // }
    // else {
    //     $('#crypto-alert-create').text('Please enter a delivery method to create an alert!')
    //     return false;
    // };
}

function crypto_chooser_success(coin, names, all) {
    // All of the things that happen when a valid coin is chosen
    var crypto_name = coin;
    var position = names.indexOf(coin);
    var btc_value = parseFloat(all[position][2]);
    var usd_value = parseFloat(all[position][1]);
    var eth_value = (parseFloat(all[position][2]) / all[names.indexOf('Ethereum')][2]).toFixed(5)
    $('#chosen_icon').removeClass().addClass('cc ' + all[position][3]);

    get_currency_rates(usd_value); // Sets CAD value
    $('.amount_chooser_coin_placeholder').text(crypto_name);
    $('.btc_value').text(btc_value + " BTC").attr('data-value', btc_value);
    $('.eth_value').text(eth_value + " ETH").attr('data-value', eth_value);;
    $('.usd_value').text('$' + usd_value + " USD").attr('data-value', usd_value);;
    $('#conversion_amounts_info').text('1 ' + crypto_name + ' =')
    $('#conversion-boxes-helptext').text(crypto_name + ' converts to:')

}


function coin_and_currency_validaion() {
    if ($('#crypto_chooser input').val() === "") {
        $('#crypto_chooser input').focus();
        return false;
    }
    if ($('#amount_chooser input').val() === "") {
        $('#crypto_chooser input').focus();
        return false;
    }
    return true;
}

function currency_choice_and_icons(currency_choice) {
    // On currency button apply chosen cuurency_choice class
    $('#currency_choice button').removeClass('currency_choice btn-info');
    currency_choice.addClass('currency_choice btn-info');

    // Clear chosen currency class from the table
    $('#conversion_amounts table tr td').removeClass('coin_current_price');
    
    $('.amount_chooser_currency_placeholder').text(currency_choice.text());
    
    // change the icon in the amount chooser to match the chosen currency
    if (currency_choice.text() == 'USD') {
        $('#chosen_currency_icon').removeClass().addClass('glyphicon glyphicon-usd')
        $('td.usd_value').addClass('coin_current_price')
    }
    else if (currency_choice.text() == 'CAD') {
        $('#chosen_currency_icon').removeClass().addClass('glyphicon glyphicon-usd')
        $('td.cad_value').addClass('coin_current_price')
    }
    else if (currency_choice.text() == 'BTC') {
        $('#chosen_currency_icon').removeClass().addClass('glyphicon glyphicon-btc')
        $('td.btc_value').addClass('coin_current_price')
    }
    else {
        $('#chosen_currency_icon').removeClass().addClass('cc ETH')
        $('td.eth_value').addClass('coin_current_price')
    }
}



// Creates an alert message underneath the tool after an alert is succesfully published
function alert_created_message() {
    var form_data = {}
    $('form').serializeArray().map(function(x) { form_data[x.name] = x.value; });
    form_data['alert_price_at_creation'] = parseFloat($('#btc_value').text())

    var delivery_methods = "";
    var direction = "";
    var message = "";
    console.log('inside alert_created_message')

    if (form_data['email'] && form_data['sms']) {
        delivery_methods = "SMS and Email alerts";
    }
    else if (form_data['email']) {
        delivery_methods = 'an email alert to ' + form_data['email'];
    }
    else {
        delivery_methods = 'an SMS alert to ' + form_data['sms'];
    }

    if (parseFloat(form_data['alert_price']) < parseFloat(form_data['alert_price_at_creation'])) {
        direction = "dropped below ";
    }
    else {
        direction = "risen above ";
    }

    message = 'New ' + form_data['coin'] + ' alert created: You will receive ' +
        delivery_methods + ' when ' + form_data['coin'] + ' has ' + direction +
        form_data['alert_price'] + ' BTC';
    console.log(message);
    return message;
}

function email_and_sms_validator() {
    var regex_email = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var regex_sms = /^\s*(?:\+?(\d{1,3}))?[- (]*(\d{3})[- )]*(\d{3})[- ]*(\d{4})(?: *[x/#]{1}(\d+))?\s*$/;
    var email = $("[name='email']").val();
    var sms = $("[name='sms']").val();
    var email_test = regex_email.test(email);
    var sms_test = regex_sms.test(sms)

    if (!sms_test && !email_test) {
        $('#crypto-alert-create').text('Please enter a delivery method to create an alert!')
        console.log('Both emai and SMS failed validation')
        return false;
    }
    else {
        $('#crypto-alert-create').text('Create Alert!');
        console.log('either email or sms or both are valid')
        return { 'email': email_test, 'sms': sms_test }
    }
}

function get_currency_rates(usd_rate) {
    $.getJSON('https://api.fixer.io/latest?base=USD', function(data) {
        var cad_rate = data['rates']['CAD'] * usd_rate;
        $('.cad_value').text('$' + cad_rate + " CAD").attr('data-value', cad_rate);;
    })
}