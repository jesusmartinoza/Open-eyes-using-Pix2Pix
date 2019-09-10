class Steps{
  constructor(wizard){
    this.wizard = wizard;
    this.steps = this.getSteps();
    this.stepsQuantity = this.getStepsQuantity();
    this.currentStep = 0;
  }

  setCurrentStep(currentStep){
    if(currentStep == 2)
      sendForm();
    this.currentStep = currentStep;
  }

  getSteps(){
    return this.wizard.getElementsByClassName('step');
  }

  getStepsQuantity(){
    return this.getSteps().length;
  }

  handleConcludeStep(){
    this.steps[this.currentStep].classList.add('-completed');
  }

  handleStepsClasses(movement){
    if(movement > 0) {
      this.steps[this.currentStep].classList.add('-active');
      this.steps[this.currentStep - 1].classList.add('-completed');
    }
    else if(movement < 0) {
      this.steps[this.currentStep + 1].classList.remove('-active');
      this.steps[this.currentStep].classList.remove('-completed');
    }
  }
}

class Panels{
  constructor(wizard){
    this.wizard = wizard;
    this.panelWidth = this.wizard.offsetWidth;
    this.panelsContainer = this.getPanelsContainer();
    this.panels = this.getPanels();
    this.currentStep = 0;

    this.updatePanelsPosition(this.currentStep);
    this.updatePanelsContainerHeight();
  }

  getCurrentPanelHeight(){
    var a = this.getPanels()[this.currentStep];
    return `${a.clientHeight}px`;
  }

  getPanelsContainer(){
    return this.wizard.querySelector('.panels');
  }

  getPanels(){
    return this.wizard.getElementsByClassName('panel');
  }

  updatePanelsContainerHeight(){
    this.panelsContainer.style.height = this.currentStep == 2 ?
                          this.getCurrentPanelHeight():
                          '365px';
  }

  updatePanelsPosition(currentStep){
    const panels = this.panels;
    const panelWidth = this.panelWidth;

    for (let i = 0; i < panels.length; i++) {
      panels[i].classList.remove(
        'movingIn',
        'movingOutBackward',
        'movingOutFoward'
      );

      if(i !== currentStep){
        if(i < currentStep) panels[i].classList.add('movingOutBackward');
        else if( i > currentStep ) panels[i].classList.add('movingOutFoward');
      }else{
        panels[i].classList.add('movingIn');
      }
    }

    this.updatePanelsContainerHeight();
  }

  setCurrentStep(currentStep){
    this.currentStep = currentStep;
    this.updatePanelsPosition(currentStep);
  }
}

class Wizard{
  constructor(obj){
    this.wizard = obj;
    this.panels = new Panels(this.wizard);
    this.steps = new Steps(this.wizard);
    this.stepsQuantity = this.steps.getStepsQuantity();
    this.currentStep = this.steps.currentStep;

    this.concludeControlMoveStepMethod = this.steps.handleConcludeStep.bind(this.steps);
    this.wizardConclusionMethod = this.handleWizardConclusion.bind(this);
  }

  updateButtonsStatus(){
    if(this.currentStep === 0)
    this.previousControl.classList.add('disabled');
    else
    this.previousControl.classList.remove('disabled');
  }

  updtadeCurrentStep(movement){
    this.currentStep += movement;
    this.steps.setCurrentStep(this.currentStep);
    this.panels.setCurrentStep(this.currentStep);

    this.handleNextStepButton();
    this.updateButtonsStatus();
  }

  handleNextStepButton(image){
    if(this.currentStep === this.stepsQuantity - 1) {
      if(image != undefined) {
        this.nextControl.innerHTML = `<a href="${image}" download>Descarga</a>`;
      } else {
        this.nextControl.innerHTML = `Descarga`;
      }

      this.nextControl.removeEventListener('click', this.nextControlMoveStepMethod);
      this.nextControl.addEventListener('click', this.concludeControlMoveStepMethod);
      this.nextControl.addEventListener('click', this.wizardConclusionMethod);
    } else {
      this.nextControl.innerHTML = 'Siguiente';

      this.nextControl.addEventListener('click', this.nextControlMoveStepMethod);
      this.nextControl.removeEventListener('click', this.concludeControlMoveStepMethod);
      this.nextControl.removeEventListener('click', this.wizardConclusionMethod);
    }
  }

  handleWizardConclusion() {
    //this.wizard.classList.add('completed');
  };

  addControls(previousControl, nextControl){
    this.previousControl = previousControl;
    this.nextControl = nextControl;
    this.previousControlMoveStepMethod = this.moveStep.bind(this, -1);
    this.nextControlMoveStepMethod = this.moveStep.bind(this, 1);

    previousControl.addEventListener('click', this.previousControlMoveStepMethod);
    nextControl.addEventListener('click', this.nextControlMoveStepMethod);

    this.updateButtonsStatus();
  }

  moveStep(movement){
    if(this.validateMovement(movement)){
      this.updtadeCurrentStep(movement);
      this.steps.handleStepsClasses(movement);
    }else{
      throw('This was an invalid movement');
    }
  }

  validateMovement(movement){
    const fowardMov = movement > 0 && this.currentStep < this.stepsQuantity - 1;
    const backMov = movement < 0 && this.currentStep > 0;

    return fowardMov || backMov;
  }

  updatePanelsPosition(){
    this.panels.updatePanelsPosition(this.currentStep);
  }
}

let wizardElement = document.getElementById('wizard');
let wizard = new Wizard(wizardElement);
let buttonNext = document.querySelector('.next');
let buttonPrevious = document.querySelector('.previous');

wizard.addControls(buttonPrevious, buttonNext);

function readPictureURL(input, id) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();


    reader.onload = function(e) {
      $(`#${id} .image-upload-wrap`).hide();

      $(`#${id} .file-upload-image`).attr('src', e.target.result);
      $(`#${id} .file-upload-content`).show();

      $(`#${id} .image-title`).html(input.files[0].name);
      $(`#processed-result .${id}`).attr('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function removeUpload(id) {
  $(`#${id} .file-upload-inputt`).replaceWith('.file-upload-input').clone();
  $(`#${id} .file-upload-content`).hide();
  $(`#${id} .image-upload-wrap`).show();
}

/**
 * Append image to form and send it to server.
 */
function sendForm() {
	console.log("Uploading file")
	var formData = new FormData();
	formData.append('input_image', $('#input-image .file-upload-input')[0].files[0]);
	formData.append('target_image', $('#target-image .file-upload-input')[0].files[0]);

  $('#processed-result').hide();
  $('#status').hide();
  $('#loader').show();
  $('#status-title').text("Processing...");

	$.ajax({
		url: '/upload',
		data: formData,
		processData: false,
		contentType: false,
		type: 'POST',
		success: function( data ) {
			console.log(data)
      $('#loader').hide()

      if(data.success) {
        $('#status-title').text("¡Listo! 🎉 🎉");
        $('#processed-result').show();
        $('#status').hide()
        $('#processed-image').attr('src', data.processed_image);
        wizard.updatePanelsPosition();
        wizard.handleNextStepButton(data.processed_image);
      } else {
        $('#status').show();
        $('#status-title').text('No pudo ser completado')
        $('#status h6').text(data.message);
      }
		}
	});
}

$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});
