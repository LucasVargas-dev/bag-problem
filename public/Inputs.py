class Inputs(object): 
  def __init__(self, nome, valor): 
    self.__nome = nome 
    self.__valor = valor 

  def __repr__(self): 
    return "nome:%s valor:%s" % (self.__nome, self.__valor)

  def get_nome(self):   
    return self.__nome

  def get_valor(self): 
    return self.__valor