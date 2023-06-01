import random

def genRandomResults():
    randomNum = random.randint(45, 100)

    sicknessPhase = None
    symptonsPhase = None

    if randomNum > 50:
        sicknessPhase = "O animal se encontra na fase ativa de infecção. A fase ativa é caracterizada pela presença de lesões cutâneas típicas da doença, como áreas circulares de perda de pelos, descamação e crostas."
        symptonsPhase = "As complicações comuns nessa fase incluem coceira intensa, irritação da pele e possível disseminação da infecção para outros animais em contato próximo."
    if randomNum == 50:
        sicknessPhase = "O animal pode se encontrar na fase inicial ou avançada. Na fase inicial, podem não haver lesões visíveis, mas o fungo pode estar presente na pele. Já na fase avançada, podem ocorrer lesões cutâneas evidentes."
        symptonsPhase = "As complicações dependerão do estágio da infecção, variando de leves a moderadas."
    if randomNum < 50:
        sicknessPhase = "O animal pode se encontrar na fase inicial ou não estar infectado. Na fase inicial, podem não haver lesões visíveis, mas o fungo pode estar presente na pele."
        symptonsPhase = "Caso não esteja infectado, não apresenta complicações."
    
    return {
        'results': randomNum,
        'currentPhase': sicknessPhase,
        'symptonsPhase': symptonsPhase
    }