var ngds=ngds||{};function callRating(a,d,c){var b=confirm(a);if(b){$.ajax({url:"/ngds/rating_submit",type:"POST",data:{rpackageId:c,ratingValue:d},success:function(e){window.location.reload()}})}}(function(){$(document).ready(function(){var c;$(".dropdown").focus(function(){c=$(this).val()}).change(function(){$(this).blur();var e=confirm("Are you sure you want to change the role?");if(e){var d="#"+$(this)[0].id.substr(5);$(d).submit()}else{$(this).val(c);return false}});$("#read-only-form :input").attr("readonly","readonly");$("#read-only-form :checkbox").attr("disabled","disabled");var a=$("input.unique");a.click(function(){a.filter(":checked").not(this).removeAttr("checked")});$("#manage-nodes-table tr:odd").css("background-color","#fff6f6");$(".not-implemented").click(function(d){ngds.not_implemented_popup_active=true;$("#not-implemented-popup").show();return false});$(document).click(function(){if(ngds.not_implemented_popup_active===true){ngds.not_implemented_popup_active=false;$("#not-implemented-popup").hide()}if(b()){$(".login-popup").hide()}});$(document).keyup(function(d){if(d.keyCode===27&&ngds.not_implemented_popup_active){$("#not-implemented-popup").hide()}});(function(){$(".login-in").click(function(){if(b()){$(".login-popup").hide()}else{$(".login-popup").show()}return false});$(document).keyup(function(d){if(d.keyCode===27&&b()){$(".login-popup").hide()}});$("#login-popup").click(function(){return false})})();function b(){return($(".login-popup").css("display")!=="none")}$("#field-lang-select").change(function(){$("#change-language").click()})})})();