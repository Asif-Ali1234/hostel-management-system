var skill_count=2,strength_count=2,intern_count=2,job_count=2,training_count=2,project_count=2,ad_count=2,tab_count=2;
    function copy_details(d_id,o_id)
	{
		var dup=document.getElementById(d_id).innerHTML;
		document.getElementById(o_id).value=dup;
	}
	copy_details('d_name','hid_name')
	copy_details('d_mail','hid_mail')
	copy_details('d_number','hid_number')
	copy_details('d_address','hid_address')
	function getChecked()
	{
		document.getElementById('value_box1').value=tab_count;
		for(var i=1;i<=5;i++)
		{
		   var check=document.getElementById('radio'+i.toString());
			if(check.checked==true)
			{
				document.getElementById('hid_c_o').value=document.getElementById('radio_label'+i.toString()).innerHTML;
			}
			else if(document.getElementById('radio6').checked==true)
			{
				document.getElementById('hid_c_o').value=document.getElementById('radio_label6').value;
			}
		}
		var i1_data=document.getElementById('degree21').value;
		alert("i1 data : "+i1_data)
		var i2_data=document.getElementById('degree22').value;
		alert("i2 data : "+i2_data)
		var i3_data=document.getElementById('degree23').value;
		alert("i3 data : "+i3_data)
		var i4_data=document.getElementById('degree24').value;
		alert("i4 data : "+i4_data)
	}
		  function add_skill(text_id,trash_id,after_id,group_id,count)
		  { 
			var string_count=count.toString();
			var ic=document.createElement("i");
			ic.classList.add("fas","fa-trash-alt","icon");
			ic.id=trash_id+string_count;
			ic.style.marginTop="0.7em"
			ic.addEventListener("mouseover",function(){
			  show_trash(true,trash_id+string_count)
			},false);
			ic.addEventListener("mouseout",function(){
			  show_trash(false,trash_id+string_count)
			},false);
			var box=document.createElement("input");
			box.classList.add("form-control")
			box.type="text";
			box.id=text_id+string_count;
			box.style.marginTop="1em"
			box.addEventListener("mouseover",function(){
			  show_trash(true,trash_id+string_count)
			},false);
			box.addEventListener("mouseout",function(){
			  show_trash(false,trash_id+string_count)
			},false);
			ic.addEventListener("click",function(){
			  delete_textbox(box.id,ic.id,text_id,trash_id,count);
			},false);
			var p=document.getElementById(group_id);
			var c=document.getElementById(after_id);
			p.insertBefore(box,c);
			var dp=document.getElementById(text_id+string_count);
			p.insertBefore(ic,dp);
			if(text_id=='s')
			{
				box.placeholder="Enter Your Skill"
				skill_count++;
			}
			else if(text_id=='ds'){
				box.placeholder="Enter Your Strength"
				strength_count++;
			}
			else if(text_id=='intern'){
				box.placeholder="Enter Your Internship Details"
				intern_count++;
			}
			else if(text_id=='job'){
				box.placeholder="Enter Your Job Details"
				job_count++;
			}
			else if(text_id=='training'){
				box.placeholder="Enter Your Training Details"
				training_count++;
			}
			else if(text_id=='project'){
				box.placeholder="Enter Your Project Details"
				project_count++;
			}
			else if(text_id=='ad'){
				box.placeholder="Enter Your Additional Details"
				ad_count++;
			}
		  }
		  function add_degree()
		  {
			var li=document.createElement('li');
			var string_count=tab_count.toString();
			li.id="List"+string_count;
			li.classList.add('nav-item');
			var tabs=document.getElementById('tabs');
			var ad_link=document.getElementById('ad_link');
			tabs.insertBefore(li,ad_link);
			var anchor=document.createElement('a');
			anchor.classList.add('nav-link');
			li.appendChild(anchor);
			anchor.setAttribute("data-toggle","tab");
			anchor.id="anchor"+string_count;
			anchor.href="#degree"+string_count;
			anchor.innerHTML="Degree"+string_count;
			var div=document.createElement('div');
			div.id="degree"+string_count;
			div.classList.add("form-group","tab-pane","fade");
			/*----first input----*/	
			var input1=document.createElement('input');
			input1.id='degree'+string_count+'1';
			input1.placeholder="Enter your degree"
			input1.classList.add('form-control')
			input1.style.marginTop='1.2em';
			input1.name="degreename"+string_count+'1';
			/*----second input----*/	
			var input2=document.createElement('input');
			input2.id='degree'+string_count+'2';
			input2.placeholder="Enter your college name"
			input2.classList.add('form-control');
			input2.style.marginTop='1.2em';
			input2.name="degreename"+string_count+'2';
			/*----third input----*/	
			var input3=document.createElement('input');
			input3.id='degree'+string_count+'3';
			input3.placeholder="Enter your percentage"
			input3.classList.add('form-control');
			input3.style.marginTop='1.2em';
			input3.name="degreename"+string_count+'3';
			/*----fourth input----*/	
			var input4=document.createElement('input');
			input4.id='degree'+string_count+'4';
			input4.placeholder="Enter year of pass"
			input4.classList.add('form-control');
			input4.style.marginTop='1.2em';
			input4.name="degreename"+string_count+'4';
			div.appendChild(input1);
			div.appendChild(input2);
			div.appendChild(input3);
			div.appendChild(input4);
			var p_div=document.getElementById('tabcontent');
			p_div.appendChild(div);
			document.getElementById('value_box1').value=tab_count;
			tab_count++;
		 }
		 function delete_tab()
		 {
			var string_count=(tab_count-1).toString();
			if(parseInt(string_count)>1)
			{
				var li=document.getElementById("List"+string_count);
				var del1=document.getElementById('anchor'+string_count);
				del1.remove();
				li.remove();
				var div=document.getElementById('degree'+string_count);
				var input1=document.getElementById('degree'+string_count+'1');
				var input2=document.getElementById('degree'+string_count+'2');
				var input3=document.getElementById('degree'+string_count+'3');
				var input4=document.getElementById('degree'+string_count+'4');
				input1.remove();
				input2.remove();
				input3.remove();
				input4.remove();
				div.remove();
				tab_count--;
			}	
		 }
		 function delete_textbox(box_id,trash_id,ides,trash_ides,count)
		 {
		   var delete_box_count=parseInt(box_id.charAt(box_id.length-1));
		   var delete_trash_count=parseInt(box_id.charAt(box_id.length-1));
		   var p=document.getElementById(box_id);
		   var q=document.getElementById(trash_id);
		   p.remove();
		   q.remove();
		   for(var i=delete_box_count;i<count-1;i++)
		   {
			  var bc=document.getElementById(ides+(i+1).toString());
			  bc.id=ides+i.toString();
		   }
		   for(var i=delete_trash_count;i<count-1;i++)
		   {
			  var bc=document.getElementById(trash_ides+(i+1).toString());
			  bc.id=trash_ides+i.toString();
		   }
		   count--;
		 }
		 function clear_text(id,a)
		 {
			var clearing=document.getElementById(id)
			if(clearing.value=='')
			{
				alert("Already Cleared");
			}
			else{
			  clearing.value='';
			}
			clearing.placeholder="Enter your "+a;
		 }
		 function show_trash(bool,trash)
		 {
		   var t=document.getElementById(trash);
		   if(bool==true)
		   t.style.display="block"
		   else
			 t.style.display="none";
		 }
		 function selectco(){
		   if(document.getElementById('radio6').checked==true)
		   {
			 document.getElementById('radio_label6').style.display="block";
		   }
		   else
			  document.getElementById('radio_label6').style.display="none";
		 }