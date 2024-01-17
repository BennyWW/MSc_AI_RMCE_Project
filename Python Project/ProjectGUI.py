# Other Scripts
import Project_GA as GeneticAlgorithm
import Prediction_Model as PredModel

# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

# region Run the unity game
def RunGame():
    # Specify the path
    path = "Unity Game Build/MSc_AI_RMCE__Project.exe"

    try:
        # Run the exe file
        subprocess.Popen(path)
    except FileNotFoundError:
        print(f"Error: The exe file '{path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# endregion

def Main():
    newData = []

    def on_canvas_configure(event):
        surveyCanvas.configure(scrollregion=surveyCanvas.bbox("all"))

    def on_mouse_wheel(event):
        surveyCanvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_arrow_keys(event):
        if event.keycode == 113:  # Up arrow key
            surveyCanvas.yview_scroll(-1, "units")
        elif event.keycode == 114:  # Down arrow key
            surveyCanvas.yview_scroll(1, "units")

    def GetResponses():
        for x in range(0, len(questions)):
            newData.append(float(questions[x].value))
        print(newData)
        model = PredModel
        predictedCluster = model.PredictCluster('ANN_PredictionModel.h5', newData)
        newData.clear()

        clustersInfo = GeneticAlgorithm.SetUpGame(predictedCluster, False)
        messagebox.showinfo("Personality Test Results",
                            f'Predicted Cluster: \tCluster {predictedCluster+1}'
                            f'\nCluster Info:'
                            f'\n  Openness:\t\t{clustersInfo[predictedCluster - 1]["O"]}%'
                            f'\n  Conscientiousness:\t{clustersInfo[predictedCluster - 1]["C"]}%'
                            f'\n  Extroversion:\t\t{clustersInfo[predictedCluster - 1]["E"]}%'
                            f'\n  Agreeableness:\t\t{clustersInfo[predictedCluster - 1]["A"]}%'
                            f'\n  Neuroticism:\t\t{clustersInfo[predictedCluster - 1]["N"]}%')
        runGA = messagebox.askyesnocancel('Run Genetic Algorithm',
                                          'Proceed to run Genetic Algorithm? (This might take a few sec/min. '
                                          'You will see a plotted history of the operation when it is done.)')
        print(runGA)
        if runGA:
            GeneticAlgorithm.SetUpGame(predictedCluster+1, True)
            environ_info = ''
            with open('Environment_Info.txt', 'r') as file:
                # Read the entire content of the file into a string
                environ_info = file.read()
            messagebox.showinfo('In-Game Environment Information',
                                "Genetic Algorithm generated the in-game Environment for you. Here's a summary:\n"+
                                environ_info)

            runGame = messagebox.askyesnocancel('Run Game',
                                                'Genetic Algorithm operation is done. Proceed to run the game? (This will launch the Unity game)')
            if runGame:
                RunGame()

    # Create Window
    root = tk.Tk()
    root.title('OCEAN Personality Test')
    root.geometry('1000x800')

    # Label/Instruction
    instruction = ('Hi, please fill up the survey to predict your Gamer Preference Group/Cluster.\n'
                   '(1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree)')
    label = tk.Label(root, text=instruction, font=('Arail', 16))
    label.pack()

    # Create question class
    class Question:
        def __init__(self):
            self.Trait = ''
            self.questionTxt = ''
            self.value = 1

        def SetValue(self, value):
            self.value = value

    # Questions dictionary
    OCEAN_qns = {
        "Extroversion": [
            "I am the life of the party.",
            "I don't talk a lot.",
            "I feel comfortable around people.",
            "I keep in the background.",
            "I start conversations.",
            "I have little to say.",
            "I talk to a lot of different people at parties.",
            "I don't like to draw attention to myself.",
            "I don't mind being the center of attention.",
            "I am quiet around strangers.",
        ],
        "Neuroticism": [
            "I get stressed out easily.",
            "I am relaxed most of the time.",
            "I worry about things.",
            "I seldom feel blue.",
            "I am easily disturbed.",
            "I get upset easily.",
            "I change my mood a lot.",
            "I have frequent mood swings.",
            "I get irritated easily.",
            "I often feel blue.",
        ],
        "Agreeableness": [
            "I feel little concern for others.",
            "I am interested in people.",
            "I insult people.",
            "I sympathize with others' feelings.",
            "I am not interested in other people's problems.",
            "I have a soft heart.",
            "I am not really interested in others.",
            "I take time out for others.",
            "I feel others' emotions.",
            "I make people feel at ease.",
        ],
        "Conscientiousness": [
            "I am always prepared.",
            "I leave my belongings around.",
            "I pay attention to details.",
            "I make a mess of things.",
            "I get chores done right away.",
            "I often forget to put things back in their proper place.",
            "I like order.",
            "I shirk my duties.",
            "I follow a schedule.",
            "I am exacting in my work.",
        ],
        "Openness": [
            "I have a rich vocabulary.",
            "I have difficulty understanding abstract ideas.",
            "I have a vivid imagination.",
            "I am not interested in abstract ideas.",
            "I have excellent ideas.",
            "I do not have a good imagination.",
            "I am quick to understand things.",
            "I use difficult words.",
            "I spend time reflecting on things.",
            "I am full of ideas.",
        ]
    }

    questions = []
    for trait in OCEAN_qns:
        for trait_qn in OCEAN_qns[trait]:
            qn = Question()
            qn.Trait = trait
            qn.questionTxt = trait_qn
            questions.append(qn)

    surveyFrame = ttk.Frame(root)
    surveyFrame.pack(padx=0, pady=10, fill=tk.BOTH, expand=True)

    surveyCanvas = tk.Canvas(surveyFrame, bg="white")
    surveyCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(surveyFrame, orient=tk.VERTICAL, command=surveyCanvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    surveyCanvas.configure(yscrollcommand=scrollbar.set)

    surveyQns = ttk.Frame(surveyCanvas)
    surveyCanvas.create_window((0, 0), window=surveyQns, anchor=tk.NW)

    for i in range(0, len(questions)):
        ttk.Label(surveyQns, text=f'{i + 1}.\t{questions[i].questionTxt}').grid(row=i, column=0, sticky="w")
        tk.Scale(surveyQns, from_=1, to=5, orient=tk.HORIZONTAL, length=200, command=questions[i].SetValue).grid(row=i,
                                                                                                                 column=1,
                                                                                                                 sticky="w")

    # Bind the canvas to update scroll region
    surveyQns.bind("<Configure>", on_canvas_configure)

    # Bind mouse wheel and arrow key events to the canvas
    surveyCanvas.bind("<MouseWheel>", on_mouse_wheel)
    surveyCanvas.bind("<Up>", on_arrow_keys)
    surveyCanvas.bind("<Down>", on_arrow_keys)

    submitBtn = tk.Button(root, text='Predict', highlightcolor='red', font=('Arial', 10), command=GetResponses,
                          padx=100, pady=20)
    submitBtn.pack()

    root.mainloop()


if __name__ == "__main__":
    Main()
