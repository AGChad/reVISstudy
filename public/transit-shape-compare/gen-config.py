import revisitpy as rvt

full_sequence = []

shapes = ["rect", "circle", "triangle", "plus", "diamond", "badge", "cresent"]
transit = ["walk", "bicycle", "car", "train", "plane", "bus", "boat"]

study_metadata = rvt.studyMetadata(
    title = "Comparing Shapes and Modes of Transit",
    version = "development",
    authors = [
        "The reVISit Team",
        "The reVISit Community",
        "Ava Chadbourne, Sam Randa, Ivy Bixler"
    ],
    date = "2025-02-05",
    description = "This study asks you to compare various shapes and modes of transit",
    organizations = [
      "University of Utah",
      "WPI",
      "University of Toronto",
      "Some really tired college kids"
    ]
)

ui_config = rvt.uiConfig(
    contactEmail="contact@revisit.dev",
    helpTextPath="./transit-shape-compare/assets/help.md",
    logoPath="./revisitAssets/revisitLogoSquare.svg",
    withProgressBar=True,
    autoDownloadStudy=False,
    autoDownloadTime=5000,
    sidebar=False
)

welcome = rvt.component(
    component_name__='welcome',
    type= "markdown",
    path ="./transit-shape-compare/assets/welcome.md",
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
    path="./transit-shape-compare/assets/shape.html"
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