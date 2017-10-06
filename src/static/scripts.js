$(function() {
    
    
    // Currency choice buttons and currency icon changer
    $('#currency_choice button').click(function() {
        var currency_choice = $(this).text()
        currency_choice_and_icons(currency_choice)
    });

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
                if (coin === null || ($.inArray(coin, names) == -1))
                    $(this).val(''); /* clear the value */
                $(this).attr('placeholder', 'Please choose a coin from the dropdown');
            }
        });

        $('#crypto_chooser').on('focusout', function(e) {
            var crypto_name = $(this).val();
            var position = names.indexOf($(this).val());
            var btc_value = parseFloat(all[position][2]);
            var usd_value = parseFloat(all[position][1]);
            var eth_value = (parseFloat(all[position][2]) / all[names.indexOf('Ethereum')][2]).toFixed(5)
            get_currency_rates(usd_value);
            $('#chosen_icon').removeClass().addClass('cc ' + all[position][3]);

            $('.btc_value').text(btc_value + " BTC");
            $('.eth_value').text(eth_value + " ETH");
            $('.usd_value').text('$' + usd_value + " USD");
            $('#conversion_amounts_info').text('1 ' + crypto_name + ' =')
            $('#conversion-boxes-helptext').text(crypto_name + ' converts to:')

        });
    });


    // Submit form data
    $('#crypto-alert-create').click(function() {
        // Validate coin and currency boxes not empty
        if (!coin_and_currency_validaion()) {return;}
        
        // Validate email and/or SMS
        var email_and_sms = email_and_sms_validator()
        console.log(email_and_sms);
        if (!email_and_sms['email'] && !email_and_sms['sms']) {
            return;
        }

        var form_data = $('form').serializeArray()
        var coin_current_price = parseFloat($('#btc_value').text());
        var coin_alert_price = parseFloat($("[name='btc_alert_price']").val());

        // Add BTC current price to form data
        form_data.push({ 'name': 'btc_price_at_creation', 'value': coin_current_price })

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
        // Populate the successful alert info box
        submit_form_alert_message(email_and_sms['email'], email_and_sms['sms'])
        
        
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
});

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
    // On press any currency choice button remove the chosen class and then apply it to pressed button
    $('#currency_choice button').removeClass('currency_choice btn-info');
    $(this).addClass('currency_choice btn-info');

    // change the icon in the amount chooser to match the chosen currency
    if (currency_choice == 'USD' || currency_choice == 'CAD') {
        $('#chosen_currency_icon').removeClass().addClass('glyphicon glyphicon-usd')
    }
    else if (currency_choice == 'BTC') {
        $('#chosen_currency_icon').removeClass().addClass('glyphicon glyphicon-btc')
    }
    else {
        $('#chosen_currency_icon').removeClass().addClass('cc ETH')
    }
}

// Creates an alert message underneath the tool after an alert is succesfully published
function alert_created_message() {
    var form_data = {}
    $('form').serializeArray().map(function(x) { form_data[x.name] = x.value; });
    form_data['btc_price_at_creation'] = parseFloat($('#btc_value').text())

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

    if (parseFloat(form_data['btc_alert_price']) < parseFloat(form_data['btc_price_at_creation'])) {
        direction = "dropped below ";
    }
    else {
        direction = "risen above ";
    }

    message = 'New ' + form_data['coin'] + ' alert created: You will receive ' +
        delivery_methods + ' when ' + form_data['coin'] + ' has ' + direction +
        form_data['btc_alert_price'] + ' BTC';
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

function submit_form_alert_message(validated_contact_data) {
    var direction = ""
    var currency = $('#crypto_chooser input').val();
    var btc_value_now = parseFloat($('#btc_value').text());
    var btc_alert_price = $('[name="btc_alert_price"]').val();
    var email = validated_contact_data[0]
    var sms = validated_contact_data[1]

    // Establish if the alert is for a higher price or a lower price
    if (currency && btc_alert_price) {
        if (parseFloat(btc_value_now) > parseFloat(btc_alert_price)) {
            direction = " when its value drops below " + btc_alert_price + "BTC";
        }
        else {
            direction = " when its value has risen above " + btc_alert_price + "BTC";
        }
    };
    // Update the alert message with the right contact data
    if (email && sms) {
        $('#crypto-alert-create').text('Send me both SMS and EMAIL alerts for ' + currency + direction)
        return true;
    }
    else if (email && !sms) {
        $('#crypto-alert-create').text('Send me an EMAIL alert for ' + currency + direction)
        return true;
    }
    else if (sms && !email) {
        $('#crypto-alert-create').text('Send me an SMS alert for ' + currency + direction)
        return true;
    }
    else {
        $('#crypto-alert-create').text('Please enter a delivery method to create an alert!')
        return false;
    };
}


function get_currency_rates(usd_value) {
    $.getJSON('https://api.fixer.io/latest?base=USD', function(data) {
        var cad_rate = data['rates']['CAD'] * usd_value;
        $('.cad_value').text('$' + cad_rate + " CAD");
    })
}