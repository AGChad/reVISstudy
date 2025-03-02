import revisitpy as rvt
import revisitpy_server as rs
import random

full_sequence = []

shapes = ["rect", "circle", "triangle", "plus", "diamond", "badge", "cresent"]
transit = ["walk", "bicycle", "car", "train", "plane", "bus", "boat"]

study_metadata = rvt.studyMetadata(
    title = "A tutorial that you will build with us",
    version = "development",
    authors = [
      "The reVISit Team",
      "The reVISit Community",
      "You :)"
    ],
    date = "2025-02-05",
    description = "This tutorial will teach you how to create a reVISit study and use all of the features that reVISit has to offer.",
    organizations = [
      "University of Utah",
      "WPI",
      "University of Toronto",
      "You :)"
    ]
)

ui_config = rvt.uiConfig(
    contactEmail="contact@revisit.dev",
    helpTextPath="./public/tutorial-hello-world/assets/help.md",
    logoPath="./public/revisitAssets/revisitLogoSquare.svg",
    withProgressBar=True,
    autoDownloadStudy=False,
    autoDownloadTime=5000,
    sidebar=False
)

welcome = rvt.component(
    component_name__='welcome',
    type= "markdown",
    path ="./public/tutorial-hello-world/assets/welcome.md",
    response = []
)


base_response = rvt.response(
    id="html-response",
    prompt=  "Answer:",
    location = "belowStimulus",
    type = "slider",
    options = [
    {
        "label": "Unrelated",
        "value": 0
    },
    {
        "label": "Closely Related",
        "value": 10
    }
    ],

    startingValue = 5
)

base_component = rvt.component(
    component_name__='shape-word-compare',
    type='website',
    response=[base_response],
    path="./public/tutorial-hello-world/assets/shape.html"
)

id = 0
for shape in shapes:
    for type in transit:
        temp_name = 'shape-word-compare-' + str(id)
        temp_component = rvt.component(
            base__=base_component,
            component_name__=temp_name,
            description="Rate the similarity between the shape and the word",
            parameters = {
                "shape": shape,
                "text": type
            }
        )

        full_sequence.append(temp_component)
        id += 1

first_sequence = rvt.sequence(
    order='fixed',
    components=[welcome]
)
second_sequence = rvt.sequence(
    order='random',
    components=full_sequence
)

sequence = first_sequence + second_sequence

study = rvt.studyConfig(
    schema="https://raw.githubusercontent.com/revisit-studies/study/v2.0.2/src/parser/StudyConfigSchema.json",
    uiConfig=ui_config,
    studyMetadata=study_metadata,
    sequence=sequence
)

#print(study)

with open("config.txt", 'w') as file:
    file.write(str(study))

# process = rs.serve()
# w = rvt.widget(study, server=True)
# w