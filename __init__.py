from importlib import reload
import main

i = str(input("Load VOICE? "))

if 'y' in i:
    t_obj = main.Base()
    #t_obj.speak('Initializing VOICE dependencies...')
    #print('Initializing VOICE dependencies...')

    MODEL = main.Model(t_obj.dirs['model'])
    REC = main.KaldiRecognizer(MODEL, 16000)
    P = main.pyaudio.PyAudio()

    del t_obj
    print("Done!")

else:
    MODEL, REC, P = None, None, None


def run():
    global MODEL, REC, P

    reload(main)
    
    obj = main.Main()

    obj.model = MODEL
    obj.rec = REC
    obj.p = P

    obj.start_main()

    MODEL = obj.model
    REC = obj.rec
    P = obj.p
    
    inp = str(input('Type "exit" to exit | Click Enter to reload... : '))
    
    if "exit" in inp:
        return
    else:
        run()


if __name__ == "__main__":
    run()
