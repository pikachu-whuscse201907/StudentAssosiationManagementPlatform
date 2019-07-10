def veri(username, password, conpass):
              "verify the validity"
              if password != conpass:
                     return "please check your password and confirmed password!"
              elif len(username) < 4:
                     return "your username is too short. The username must be more than 4 chars!"
              elif len(str(password)) < 6:
                     return "your password is too short. The password must be more than 6 chars!"
              else:
                     for each in username:
                            if each >= 'A' and each <= 'Z':
                                   continue
                            elif each >= "a" and each <= "z":
                                   continue
                            elif each >= '0' and each <= '9':
                                   continue
                            elif each == "_":
                                   continue
                            else:
                                   return "Your username includes invalid char!"
              person = people.objects.get(name = username)
              if person == None:
                     pass
              else:
                     return "The username has been registered!"
              return True
              
