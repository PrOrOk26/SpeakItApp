const MEANINGS_DATA = "meaning_tests"
const MEANINGS_TEST_RESULTS_DATA = "meanings_test_result"

const NEUTRAL_STATE = 0
const RIGHT_ANSWER_STATE = 1
const WRONG_ANSWER_STATE = 2

const RIGHT_ANSWER_IMAGE_REF = "http://127.0.0.1:8000/static/test_voc/img/icons8-checkmark.svg"
const WRONG_ANSWER_IMAGE_REF = "http://127.0.0.1:8000/static/test_voc/img/rejected.svg"
const PROMPT_EXAMPLE_PHRASE  = "Look at the example to memorise better!"

const TESTS_MAIN_PAGE_URL = "{% url 'lang:test_voc:testmain' user.username %}"

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    }
	});

$(document).ready( function() {
    changeFooterState(NEUTRAL_STATE)

    const url_tests = "get_questions/"
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
            sessionStorage.setItem(MEANINGS_TEST_RESULTS_DATA, JSON.stringify([]))
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
    
    $("#question-text").text("What does \'" + test_to_show.word + "\' mean?")
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
        input.setAttribute('name', 'choice')

        if(i == 0)
            input.checked = true

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

// fires when the "answer" button is pressed(color changes, example showing!)
function onAnswerMade(isSkipped = false) {

    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    var current_test_to_check = tests[0]

    var radio_inputs = $(".custom-control-input")
    var choosen_answer = ""
    for (let i = 0; i < radio_inputs.length; i++) {
        if($(radio_inputs[i]).is(":checked")) {
            let id = $(radio_inputs[i]).attr("id")
            let label = "".concat("label[for=\'", id, "\']")
            let radio_label = $(label)
            choosen_answer = radio_label.text()
            break
        }
    }

    if(choosen_answer.length == 0 && !isSkipped) {
        alert("Please,choose an answer!")
        return
    }

    let example_to_show = current_test_to_check.word_examples[0] || "You don't have any examples yet!"

    if (choosen_answer == current_test_to_check.right_meaning) {
        saveAnswer(RIGHT_ANSWER_STATE)
        tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
        if(!isSkipped && tests.length > 0)
            changeFooterState(RIGHT_ANSWER_STATE)
        else if(!isSkipped && tests.length == 0)
            changeFooterState(RIGHT_ANSWER_STATE, true)
    }
    else {
        saveAnswer(WRONG_ANSWER_STATE)
        tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
        if(!isSkipped && tests.length > 0)
            changeFooterState(WRONG_ANSWER_STATE)
        else if(!isSkipped && tests.length == 0)
            changeFooterState(WRONG_ANSWER_STATE, true)
    }

    if(!isSkipped)
        setFooterExample(current_test_to_check.word, example_to_show)

    if(isSkipped && tests.length > 0)
        onNextQuestion()
    else if(isSkipped && tests.length == 0)
        changeFooterState(NEUTRAL_STATE, true)
    
}

//fires when the next question is shown
function onNextQuestion() {
    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    var results = JSON.parse(sessionStorage.getItem(MEANINGS_TEST_RESULTS_DATA))

    clearQuestionChoices()
    insertNextTest()
    setTestProgressBar(results.length / (tests.length + results.length))

    changeFooterState(NEUTRAL_STATE, false)
}

//fires then the test is over
function onFinish() {
    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    //send AJAX if the test is over,show result()
    let test_results = JSON.parse(sessionStorage.getItem(MEANINGS_TEST_RESULTS_DATA))

    if(tests.length != 0) {
        tests.forEach( (elem) => 
            test_results.push( { word_id: elem.word_id,
                                 times_asked: 1,
                                 times_right: 0 })
        )
    }


    const url_process_results = "process_results/"
        $.ajax({
            type: "POST",
            url: url_process_results,
            data: {
            'results': JSON.stringify(test_results)
            },
            dataType: 'json',
            success: function (data) {
                var resultHTML = data.resultHTML
                showTestResult(resultHTML)
            }
        });
}

function changeFooterState(state = NEUTRAL_STATE, isLastWord = false) {

    $("#btn-end-test a").attr("onclick", "onFinish()")

    if(state == NEUTRAL_STATE) {
        $("#footer").css("background-color", "rgb(231, 231, 231)")

        $("#question-result").text("")
        $("#example-header").text("")
        $("#example-text").text("")
        $("#result-icon").attr("src", "")
        $("#result-icon").hide()


        if(!isLastWord) {
            $("#btn-skip").attr("onclick", "onAnswerMade(true)")
            $("#btn-skip").show()
            $("#btn-check").text("Check my answer")
            $("#btn-check").attr("onclick", "onAnswerMade()")
            $("#btn-check").show()
        }
        else {
            $("#btn-skip").hide()
            $("#btn-check").text("Finish")
            $("#btn-check").attr("onclick", "onFinish()")
            $("#btn-check").show()
        }
    }
    else if (state == RIGHT_ANSWER_STATE) {
        $("#footer").css("background-color", "green")

        $("#question-result").text("Right")
        $("#example-header").text(PROMPT_EXAMPLE_PHRASE)
        $("#result-icon").attr("src", RIGHT_ANSWER_IMAGE_REF)
        $("#result-icon").show()

        $("#btn-skip").hide()

        if(!isLastWord) {
            $("#btn-check").text("Next")
            $("#btn-check").attr("onclick", "onNextQuestion()")
            $("#btn-check").show()
        }
        else {
            $("#btn-check").text("Finish")
            $("#btn-check").attr("onclick", "onFinish()")
            $("#btn-check").show()
        }
    }
    else if (state == WRONG_ANSWER_STATE) {
        $("#footer").css("background-color", "red")

        $("#question-result").text("Wrong")
        $("#example-header").text(PROMPT_EXAMPLE_PHRASE)
        $("#result-icon").attr("src", WRONG_ANSWER_IMAGE_REF)
        $("#result-icon").show()

        $("#btn-skip").hide()

        if(!isLastWord) {
            $("#btn-check").text("Next")
            $("#btn-check").attr("onclick", "onNextQuestion()")
            $("#btn-check").show()
        }
        else {
            $("#btn-check").text("Finish")
            $("#btn-check").attr("onclick", "onFinish()")
            $("#btn-check").show()
        }
    }

}

//this method is used when we need to set a footer example
function setFooterExample(word, example_to_show) {
    const ARTICLES = ['a', 'the', 'to', ]
    if(example_to_show == "You don't have any examples yet!")
        $("#example-text").append("<span style=\"font-weight: bold\">Try to add one to improve faster!</span>")
    else if(example_to_show.length >= word.length) {
        var word_tokens = word.split(' ')
        var example_tokens = example_to_show.split(' ')
        word_tokens = word_tokens.filter( elem => !ARTICLES.includes(elem.toLowerCase()) )
        example_tokens = example_tokens.map( (ex_toc) => {
            for (let word_tok of word_tokens) {
                if(ex_toc.toLowerCase().includes(word_tok.toLowerCase()))
                    ex_toc = ex_toc.replace(ex_toc, "".concat("<span class=\"underlined\">", ex_toc, "</span>"))
            }
            return ex_toc
        })
        example_to_show = example_tokens.join(' ')
        $("#example-text").append(example_to_show)
        /*
        for(let token of example_tokens) {
            if(!token.contains('span'))
                $("#example-text").append(token)
        }
                */
    }
    //$("#example-text").text(example_to_show)
    }

//this method fires when we want to save the answer
function saveAnswer(answerState) {
    var tests = JSON.parse(sessionStorage.getItem(MEANINGS_DATA))
    var results = JSON.parse(sessionStorage.getItem(MEANINGS_TEST_RESULTS_DATA))

    var test_to_save = tests[0]
    tests = tests.slice(1)
    
    if(answerState == RIGHT_ANSWER_STATE) {
        results.push({ word_id: test_to_save.word_id,
                        times_asked: 1,
                        times_right: 1 })
    }
    else if(answerState == WRONG_ANSWER_STATE) {
        results.push({ word_id: test_to_save.word_id,
            times_asked: 1,
            times_right: 0 })
    }

    sessionStorage.setItem(MEANINGS_DATA, JSON.stringify(tests))
    sessionStorage.setItem(MEANINGS_TEST_RESULTS_DATA, JSON.stringify(results))

}

//fires when the result needs to be shown
function showTestResult(resultHTML) {
    $(".progress-container").hide()
    $("#question").hide()
    $("#footer").hide()
    $("#btn-end-test a").hide()

    $("#btn-end-test").after(resultHTML)
}

function setTestProgressBar(percents) {
    $(".progress-bar").text(percents * 100 + "%")
    $(".progress-bar").attr("style", "".concat("width: ", percents * 100, "%;"))
    $(".progress-bar").attr("aria-valuenow", percents * 100)
}

function clearQuestionChoices() {
    $("#question-choices").empty()
}

