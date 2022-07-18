(function(){"use strict";var t={611:function(t,e,s){var n=s(144),i=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-app",[s("v-main",[s("check-completed")],1)],1)},o=[],r=function(){var t=this,e=t.$createElement,s=t._self._c||e;return t.loaded?s("div",[t.attempted?s("CompleteHome",{attrs:{attempt:t.attempt}}):s("UncompleteHome")],1):t._e()},a=[],l=s(9669),c=s.n(l),u=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"hide",attrs:{id:"hcom"}},[s("div",{staticClass:"container"},[s("v-row",[s("v-col",{staticStyle:{display:"flex","justify-content":"left"},attrs:{sm:"12"}},[s("v-btn",{attrs:{plain:""},on:{click:t.backButton}},[s("v-icon",{attrs:{left:""}},[t._v(" mdi-chevron-left ")]),t._v(" Back ")],1)],1)],1),s("v-row",[s("v-col",{attrs:{sm:"12"}},[s("v-card",[s("div",{staticClass:"text-h4",staticStyle:{"font-weight":"700"}},[t._v(" "+t._s(t.quizName)+" ")])])],1)],1),t._l(t.questions,(function(e,n){return s("div",{key:e.id},[s("v-row",[s("v-col",[s("QuestionView",{attrs:{question:e,getIsRandomOptions:t.getIsRandomOptions,highlightUndone:t.highlightUndone,questionNumber:n+1}})],1)],1)],1)})),s("v-row",[s("v-col",{staticClass:"justify-end d-flex",staticStyle:{"padding-bottom":"0"},attrs:{xs:"12"}},[s("v-btn",{attrs:{color:"primary"},on:{click:t.submitQuiz}},[t._v("Submit "),s("v-icon",{attrs:{right:"",dark:""}},[t._v(" mdi-send ")])],1)],1)],1),s("v-row",{staticStyle:{"margin-bottom":"3rem"}},[s("v-col",{class:{"d-flex":!0,"justify-end":!0,transparent:!t.highlightUndone},staticStyle:{"padding-top":"8px","font-weight":"700"},attrs:{xs:"12"}},[t._v(" Please attempt all questions ")])],1)],2)])},d=[],p=(s(6699),s(6486)),m=s.n(p),h=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-card",{class:{qCard:!0,highlightCard:t.highlightUndone&&!t.attempted}},[s("v-row",[s("v-col",{staticClass:"text-h5 questionText",attrs:{sm:"12"}},[t._v(" "+t._s(t.questionNumber)+". "+t._s(t.question.text)+" ")])],1),s("v-row",["mc"===t.question.type?s("div",[s("v-col",{staticClass:"inputCol mcCol",attrs:{sm:"12"}},[s("v-radio-group",{attrs:{"hide-details":""},model:{value:t.mcAnswer,callback:function(e){t.mcAnswer=e},expression:"mcAnswer"}},t._l(t.options,(function(e){return s("v-radio",{key:e.id,attrs:{value:e.id},scopedSlots:t._u([{key:"label",fn:function(){return[s("div",{staticClass:"black--text",attrs:{id:"questionOption-"+e.id.toString()}},[t._v(" "+t._s(e.text)+" ")])]},proxy:!0}],null,!0)})})),1)],1)],1):t._e(),"cb"===t.question.type?s("v-col",{staticClass:"inputCol",attrs:{sm:"12"}},t._l(t.options,(function(e){return s("v-checkbox",{key:e.id,staticClass:"cbRow",attrs:{"hide-details":"",value:e.id},scopedSlots:t._u([{key:"label",fn:function(){return[s("div",{staticClass:"black--text",attrs:{id:"questionOption-"+e.id.toString()}},[t._v(" "+t._s(e.text)+" ")])]},proxy:!0}],null,!0),model:{value:t.cbAnswer,callback:function(e){t.cbAnswer=e},expression:"cbAnswer"}})})),1):t._e(),"sa"===t.question.type?s("v-col",{staticClass:"saCol",attrs:{sm:"12"}},[s("v-text-field",{attrs:{label:"Answer"},model:{value:t.tAnswer,callback:function(e){t.tAnswer=e},expression:"tAnswer"}})],1):t._e(),"la"===t.question.type?s("v-col",{attrs:{sm:"12"}},[s("v-textarea",{attrs:{filled:"",label:"Answer"},model:{value:t.tAnswer,callback:function(e){t.tAnswer=e},expression:"tAnswer"}})],1):t._e()],1),t.highlightUndone&&!t.attempted?s("v-row",{staticClass:"text-caption questionText d-flex justify-end"},[t._v(" Please attempt this question ")]):t._e()],1)},v=[],f={responses:{},setResponse(t,e){this.responses[t]={id:t,response:e}},getLength(){return Object.keys(this.responses).length},clearResponses(){this.responses={}}},b={props:{question:Object,getIsRandomOptions:Function,highlightUndone:Boolean,questionNumber:Number},data:()=>({options:[],cbAnswer:[],mcAnswer:-1,tAnswer:"",attempted:!1}),watch:{mcAnswer(){this.attempted=!0,f.setResponse(this.question.id,this.mcAnswer)},cbAnswer(){this.attempted=!0,f.setResponse(this.question.id,this.cbAnswer)},tAnswer(){this.attempted=!0,f.setResponse(this.question.id,this.tAnswer)}},mounted(){const t=JSON.parse(this.question.optionOrder),e=[],s=this.question.options.filter((e=>!t.includes(e.id)));for(const n of t){const t=this.question.options.find((t=>t.id===n));void 0!==t&&e.push(t)}this.options=e.concat(s),this.getIsRandomOptions()&&(this.options=m().shuffle(this.options))}},w=b,q=s(1001),x=s(3453),g=s.n(x),y=s(3237),_=s(3702),C=s(2102),A=s(8978),k=s(9245),O=s(2877),Z=s(8518),S=s(4350),V=(0,q.Z)(w,h,v,!1,null,"682587da",null),R=V.exports;g()(V,{VCard:y.Z,VCheckbox:_.Z,VCol:C.Z,VRadio:A.Z,VRadioGroup:k.Z,VRow:O.Z,VTextField:Z.Z,VTextarea:S.Z});var j={components:{QuestionView:R},data(){return{quizName:"",randomOptions:!0,randomQuestions:!0,questions:[],questionOrder:"",highlightUndone:!1}},methods:{backButton(){history.back()},getIsRandomOptions(){return this.randomOptions},submitQuiz(){console.log(f.getLength()),f.getLength()===this.questions.length?(this.highlightUndone=!1,c().post("../submit/",f.responses,{withCredentials:!0,headers:{"X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value}}).then((()=>{window.location.reload()}))):this.highlightUndone=!0}},mounted(){f.clearResponses(),c().get("../doGet/").then((t=>{m().extend(this,t.data),this.randomOptions=1===this.randomOptions,this.randomQuestions=1===this.randomQuestions;const e=JSON.parse(this.questionOrder),s=[],n=this.questions.filter((t=>!e.includes(t.id)));for(const i of e){const t=this.questions.find((t=>t.id===i));void 0!==t&&s.push(t)}this.questions=s.concat(n),this.randomQuestions&&(this.questions=m().shuffle(this.questions)),document.getElementById("hcom").classList.remove("hide")}))}},N=j,T=s(557),U=s(6428),Q=(0,q.Z)(N,u,d,!1,null,null,null),B=Q.exports;g()(Q,{VBtn:T.Z,VCard:y.Z,VCol:C.Z,VIcon:U.Z,VRow:O.Z});var I=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"hide",attrs:{id:"hcom"}},[s("div",{staticClass:"container"},[s("v-row",[s("v-col",{staticStyle:{display:"flex","justify-content":"left"},attrs:{sm:"12"}},[s("v-btn",{attrs:{plain:""},on:{click:t.backButton}},[s("v-icon",{attrs:{left:""}},[t._v(" mdi-chevron-left ")]),t._v(" Back ")],1)],1)],1),s("v-row",[s("v-col",{attrs:{sm:"12"}},[s("v-card",[s("div",{staticClass:"text-h4",staticStyle:{"font-weight":"700"}},[t._v(" "+t._s(t.attempt.quizName)+" ")]),s("div",{staticClass:"text-subtitle-1",staticStyle:{"margin-left":"0.8rem"}},[t._v(" Quiz review ")])])],1)],1),t._l(t.questionAttempts,(function(t,e){return s("div",{key:t.id},[s("v-row",[s("v-col",[s("QuestionReview",{attrs:{questionAttempt:t,questionNumber:e+1}})],1)],1)],1)})),s("v-row",[s("v-col",{staticClass:"justify-end d-flex",staticStyle:{"padding-bottom":"3rem",cursor:"not-allowed"},attrs:{xs:"12"}},[s("v-btn",{attrs:{color:"primary",disabled:""}},[t._v("already submitted")])],1)],1)],2)])},z=[],E=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-card",{class:{qCard:!0,highlightCorrect:t.isCorrect&&t.question.autoGrade,highlightIncorrect:!t.isCorrect&&t.question.autoGrade}},[s("v-row",[s("v-col",{staticClass:"text-h5 questionText",attrs:{sm:"12"}},[t._v(" "+t._s(t.questionNumber)+". "+t._s(t.question.text)+" ")])],1),s("v-row",["mc"===t.question.type?s("div",[s("v-col",{staticClass:"inputCol mcCol",attrs:{sm:"12"}},[s("v-radio-group",{attrs:{"hide-details":""},model:{value:t.mcAnswer,callback:function(e){t.mcAnswer=e},expression:"mcAnswer"}},t._l(t.options,(function(e){return s("v-radio",{key:e.id,attrs:{value:e.id,disabled:""},scopedSlots:t._u([{key:"label",fn:function(){return[s("div",{staticClass:"black--text",attrs:{id:"questionOption-"+e.id.toString()}},[t._v(" "+t._s(e.text)+" ")])]},proxy:!0}],null,!0)})})),1)],1)],1):t._e(),"cb"===t.question.type?s("v-col",{staticClass:"inputCol",attrs:{sm:"12"}},t._l(t.options,(function(e){return s("v-checkbox",{key:e.id,staticClass:"cbRow",attrs:{"hide-details":"",value:e.id,disabled:""},scopedSlots:t._u([{key:"label",fn:function(){return[s("div",{staticClass:"black--text",attrs:{id:"questionOption-"+e.id.toString()}},[t._v(" "+t._s(e.text)+" ")])]},proxy:!0}],null,!0),model:{value:t.cbAnswer,callback:function(e){t.cbAnswer=e},expression:"cbAnswer"}})})),1):t._e(),"sa"===t.question.type?s("v-col",{staticClass:"saCol",attrs:{sm:"12"}},[s("v-text-field",{attrs:{label:"Answer",readonly:""},model:{value:t.tAnswer,callback:function(e){t.tAnswer=e},expression:"tAnswer"}})],1):t._e(),"la"===t.question.type?s("v-col",{attrs:{sm:"12"}},[s("v-textarea",{attrs:{filled:"",label:"Answer",readonly:""},model:{value:t.tAnswer,callback:function(e){t.tAnswer=e},expression:"tAnswer"}})],1):t._e()],1),"sa"===t.question.type&&t.question.autoGrade&&!t.isCorrect?s("v-row",{staticClass:"text-subtitle-1"},[t._v(" Correct answer: "+t._s(t.tAnswer)+" ")]):t._e(),"cb"===t.question.type&&t.question.autoGrade&&!t.isCorrect?s("v-row",{staticClass:"text-subtitle-1",staticStyle:{display:"flex","align-items":"center"}},[t._v(" Correct answer: "),t._l(t.question.options.filter((function(e){return t.question.cbAnswer.includes(e.id)})),(function(e){return s("div",{key:e.id,staticStyle:{border:"1px solid #999",padding:"0px 8px",margin:"2px 0 2px 10px","border-radius":"10px"}},[t._v(" "+t._s(e.text)+" ")])}))],2):t._e(),"mc"===t.question.type&&t.question.autoGrade&&!t.isCorrect?s("v-row",{staticClass:"text-subtitle-1"},[t._v(" Correct answer: "+t._s(t.question.options.find((function(e){return e.id==t.question.mcAnswer})).text)+" ")]):t._e(),s("v-row",{staticClass:"text-overline questionText d-flex justify-end",staticStyle:{"margin-top":"0"}},[t._v(" "+t._s(t.question.autoGrade?t.isCorrect?"Correct":"Incorrect":"Ungraded")+" ")])],1)},G=[],$={props:{questionAttempt:Object,questionNumber:Number},data:()=>({question:Object,cbAnswer:[],mcAnswer:-1,tAnswer:"",type:"",isCorrect:!1}),mounted(){m().extend(this,this.questionAttempt),this.cbAnswer=JSON.parse(this.cbAnswer),this.tAnswer=this.questionAttempt.saAnswer;const t=JSON.parse(this.question.optionOrder),e=[],s=this.question.options.filter((e=>!t.includes(e.id)));for(const n of t){const t=this.question.options.find((t=>t.id===n));void 0!==t&&e.push(t)}this.options=e.concat(s),console.log(this.question)}},F=$,P=(0,q.Z)(F,E,G,!1,null,"1e57f903",null),J=P.exports;g()(P,{VCard:y.Z,VCheckbox:_.Z,VCol:C.Z,VRadio:A.Z,VRadioGroup:k.Z,VRow:O.Z,VTextField:Z.Z,VTextarea:S.Z});var H={components:{QuestionReview:J},props:{attempt:Object},data(){return{questionAttempts:Object}},methods:{backButton(){history.back()}},mounted(){console.log(this.attempt);const t=JSON.parse(this.attempt.questionOrder),e=[],s=this.attempt.questionAttempts.filter((e=>!t.includes(e.question.id)));for(const n of t){const t=this.attempt.questionAttempts.find((t=>t.question.id===n));void 0!==t&&e.push(t)}this.questionAttempts=e.concat(s)}},L=H,M=(0,q.Z)(L,I,z,!1,null,null,null),D=M.exports;g()(M,{VBtn:T.Z,VCard:y.Z,VCol:C.Z,VIcon:U.Z,VRow:O.Z});var X={components:{UncompleteHome:B,CompleteHome:D},data(){return{attempted:!1,attempt:{},loaded:!1}},created(){c().get("http://127.0.0.1:8000/quizzes/quiz2022-06-09-11-37/getAttempt/").then((t=>{this.attempted=t.data.attempted,this.attempted&&(this.attempt=t.data.attempt),this.loaded=!0}))}},K=X,W=(0,q.Z)(K,r,a,!1,null,null,null),Y=W.exports,tt={name:"App",components:{CheckCompleted:Y},data:()=>({})},et=tt,st=s(7524),nt=s(1009),it=(0,q.Z)(et,i,o,!1,null,null,null),ot=it.exports;g()(it,{VApp:st.Z,VMain:nt.Z});var rt=s(1910);n.Z.use(rt.Z);var at=new rt.Z({theme:{themes:{light:{primary:"#db3833",accent:"#536DFE",info:"#db3833"}}}});n.Z.config.productionTip=!1,new n.Z({vuetify:at,render:t=>t(ot)}).$mount("#app")}},e={};function s(n){var i=e[n];if(void 0!==i)return i.exports;var o=e[n]={id:n,loaded:!1,exports:{}};return t[n].call(o.exports,o,o.exports,s),o.loaded=!0,o.exports}s.m=t,function(){var t=[];s.O=function(e,n,i,o){if(!n){var r=1/0;for(u=0;u<t.length;u++){n=t[u][0],i=t[u][1],o=t[u][2];for(var a=!0,l=0;l<n.length;l++)(!1&o||r>=o)&&Object.keys(s.O).every((function(t){return s.O[t](n[l])}))?n.splice(l--,1):(a=!1,o<r&&(r=o));if(a){t.splice(u--,1);var c=i();void 0!==c&&(e=c)}}return e}o=o||0;for(var u=t.length;u>0&&t[u-1][2]>o;u--)t[u]=t[u-1];t[u]=[n,i,o]}}(),function(){s.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return s.d(e,{a:e}),e}}(),function(){s.d=function(t,e){for(var n in e)s.o(e,n)&&!s.o(t,n)&&Object.defineProperty(t,n,{enumerable:!0,get:e[n]})}}(),function(){s.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){s.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){s.nmd=function(t){return t.paths=[],t.children||(t.children=[]),t}}(),function(){var t={143:0};s.O.j=function(e){return 0===t[e]};var e=function(e,n){var i,o,r=n[0],a=n[1],l=n[2],c=0;if(r.some((function(e){return 0!==t[e]}))){for(i in a)s.o(a,i)&&(s.m[i]=a[i]);if(l)var u=l(s)}for(e&&e(n);c<r.length;c++)o=r[c],s.o(t,o)&&t[o]&&t[o][0](),t[o]=0;return s.O(u)},n=self["webpackChunkmodify"]=self["webpackChunkmodify"]||[];n.forEach(e.bind(null,0)),n.push=e.bind(null,n.push.bind(n))}();var n=s.O(void 0,[998],(function(){return s(611)}));n=s.O(n)})();
//# sourceMappingURL=app.dcfa17ae.js.map