const MEANINGS_DATA = "meaning_tests"
const MEANINGS_TEST_RESULTS_DATA = "meanings_test_result"

const NEUTRAL_STATE = 0
const RIGHT_ANSWER_STATE = 1
const WRONG_ANSWER_STATE = 2

$(document).ready( function() {
    const url_tests = "test_meanings/get_tests/"
    $.ajax({
        type: "GET",
        url: url_tests,
        data: {
          'tests': 10
        },
        dataType: 'json',
        success: function (data) {
            var tests = data.tests
            sessionStorage.setItem(MEANINGS_DATA, JSON.stringify(tests))
            sessionStorage.setItem(MEANINGS_TEST_RESULTS_DATA, "")
            sessionStorage.setItem()
            insertNextTest()
        }
    });
})

function insertNextTest() {

    function shuffle(a) {
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
    }

    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    const test_to_show = tests[0]
    var choicesText = [ test_to_show.right_meaning ]
    test_to_show.word_meanings.forEach( (item) => choicesText.push(item))
    choicesText = shuffle(choicesText)

    var choicesHTML = createChoices(choicesText, choicesText.length)
    
    $("#question-text").innerText = test_to_show.question
    for(let i = 0; i < choicesHTML.length; i++)
        $("#question-choices").append(choicesHTML[i])

}

function createChoices(choicesText, amount) {
    var choicesToReturn = []
    for (let i = 0; i < amount; i++) {
        var choice = document.createElement('div');
        choice.setAttribute('class', 'custom-control custom-radio')
        var input = document.createElement('input')
        input.setAttribute('type', 'radio')
        input.setAttribute('class', 'custom-control-input')
        input.setAttribute('id', 'choice' + i)
        input.setAttribute('name', 'choice' + i)
        var label = document.createElement('label')
        label.setAttribute('class', 'custom-control-label')
        label.setAttribute('for', 'choice' + i)
        label.textContent = choicesText[i]
        choice.appendChild(input)
        choice.appendChild(label)
        choicesToReturn.push(choice)
    }
    return choicesToReturn
}

//fires when the "End test" button is pressed
function onQuit() {

}

// fires when the "answer" button is pressed(color changes, example showing!)
function onAnswerMade() {

    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    var current_test_to_check = tests[0]

    var radio_inputs = $(".custom-control-input")
    var choosen_answer = ""
    for (let i = 0; i < radio_inputs.length; i++) {
        if($(radio_inputs[i]).is(":checked"))
            let radio_label = $("label[for='" + $(radio_inputs[i]).attr("id") + "']")
            choosen_answer = radio_label.textContent
            break
    }

    if(choosen_answer.length == 0) {
        alert("Please,choose an answer!")
        return
    }

    let example_to_show = current_test_to_check.examples[0]

    if (choosen_answer == current_test_to_check.right_meaning) {
        changeFooterState(RIGHT_ANSWER_STATE)
        saveAnswer(RIGHT_ANSWER_STATE)
    }
    else {
        changeFooterState(WRONG_ANSWER_STATE)
        saveAnswer(WRONG_ANSWER_STATE)
    }

    setFooterExample(current_test_to_check.word, example_to_show)
}

function onNextQuestion() {
    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    if(tests.length == 0) {
        
    }
    //process next question, send AJAX if the test is over,show result()
}

function changeFooterState(state) {
    if(state == NEUTRAL_STATE) {
        $()
    }
    else if (state == RIGHT_ANSWER_STATE) {
        
    }
    else if (state == WRONG_ANSWER_STATE) {

    }

}

function setFooterExample(word, example_to_show) {

}

function saveAnswer(answerState) {

}
