/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
ngds.SearchResult=function(c){(function(){if(c===null||typeof c==="undefined"){throw"Expected raw_result to not be null or undefined."}})();var b;if(this.ckanlib!==null&&typeof this.ckanlib!=="undefined"){b=function(f){var d=function(g){return g};var e={author:this.ckanlib.get_responsible_party,maintainer:this.ckanlib.get_responsible_party};return e[f.type](f.id,d)}}else{b=function(e,d){return null}}var a={count:c.count,author_email:c.author_email,id:c.id,maintainer:b};return{get:function(){var e=false;var f={},d;for(argument in arguments){if(typeof arguments[argument]==="object"){e=true;f=arguments[argument]}else{d=arguments[argument]}}if(e===false){return a[d]}return a[d](f)},raw:function(){return c}}};(function(a){ngds.SearchResult.ckanlib=a})(ngds.ckanlib);
