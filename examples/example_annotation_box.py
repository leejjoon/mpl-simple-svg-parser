import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox


from mpl_simple_svg_parser import SVGMplPathIterator
import seaborn as sns
import pandas as pd


# TIOBE score from https://spectrum.ieee.org/the-top-programming-languages-2023

l = [
    ("Python", 1),
    ("Java", 0.588),
    ("C++", 0.538),
    ("C", 0.4641),
    ("JavaScript", 0.4638),
    ("C#", 0.3973)
]

df = pd.DataFrame(l, columns=["language", "score"])


sns.set_color_codes("muted")
sns.set(font_scale = 1.5)

fig, ax = plt.subplots(num=1, clear=True, layout="constrained")

sns.barplot(x="score", y="language", data=df,
            label="Tiobe Score 2023", color="b")

ax.yaxis.label.set_visible(False)
ax.set_title("TIOBE Score 2023")

# svg icons of selected language, downloaded from https://www.svgrepo.com.
icons = {
    "python": b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><defs><linearGradient id="a" x1="-133.268" y1="-202.91" x2="-133.198" y2="-202.84" gradientTransform="translate(25243.061 38519.17) scale(189.38 189.81)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#387eb8"></stop><stop offset="1" stop-color="#366994"></stop></linearGradient><linearGradient id="b" x1="-133.575" y1="-203.203" x2="-133.495" y2="-203.133" gradientTransform="translate(25309.061 38583.42) scale(189.38 189.81)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffe052"></stop><stop offset="1" stop-color="#ffc331"></stop></linearGradient></defs><title>file_type_python</title><path d="M15.885,2.1c-7.1,0-6.651,3.07-6.651,3.07V8.36h6.752v1H6.545S2,8.8,2,16.005s4.013,6.912,4.013,6.912H8.33V19.556s-.13-4.013,3.9-4.013h6.762s3.772.06,3.772-3.652V5.8s.572-3.712-6.842-3.712h0ZM12.153,4.237a1.214,1.214,0,1,1-1.183,1.244v-.02a1.214,1.214,0,0,1,1.214-1.214h0Z" style="fill:url(#a)"></path><path d="M16.085,29.91c7.1,0,6.651-3.08,6.651-3.08V23.65H15.985v-1h9.47S30,23.158,30,15.995s-4.013-6.912-4.013-6.912H23.64V12.4s.13,4.013-3.9,4.013H12.975S9.2,16.356,9.2,20.068V26.2s-.572,3.712,6.842,3.712h.04Zm3.732-2.147A1.214,1.214,0,1,1,21,26.519v.03a1.214,1.214,0,0,1-1.214,1.214h.03Z" style="fill:url(#b)"></path></g></svg>''',
    'java': b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><title>file_type_java</title><path d="M12.325,23.654s-1.07.622.761.833a16.023,16.023,0,0,0,5.8-.246,10.088,10.088,0,0,0,1.541.752c-5.481,2.349-12.405-.136-8.1-1.339" style="fill:#5382a1"></path><path d="M11.656,20.588s-1.2.888.633,1.078a22.618,22.618,0,0,0,7.481-.359,3.32,3.32,0,0,0,1.152.7c-6.627,1.938-14.009.153-9.266-1.421" style="fill:#5382a1"></path><path d="M17.3,15.388a2.051,2.051,0,0,1-.355,2.954s3.429-1.77,1.854-3.987c-1.471-2.067-2.6-3.095,3.508-6.636,0,0-9.586,2.394-5.007,7.669" style="fill:#5382a1"></path><path d="M24.552,25.921s.792.652-.872,1.157c-3.164.958-13.168,1.248-15.948.038-1-.435.874-1.038,1.464-1.164a3.8,3.8,0,0,1,.966-.108c-1.111-.783-7.181,1.537-3.083,2.2,11.176,1.812,20.372-.816,17.473-2.124" style="fill:#5382a1"></path><path d="M12.84,17.412s-5.089,1.209-1.8,1.648a38.225,38.225,0,0,0,6.731-.072c2.106-.178,4.221-.555,4.221-.555a8.934,8.934,0,0,0-1.28.685c-5.168,1.359-15.151.727-12.277-.663a9.629,9.629,0,0,1,4.407-1.042" style="fill:#5382a1"></path><path d="M21.969,22.515c5.253-2.73,2.824-5.353,1.129-5a3.932,3.932,0,0,0-.6.161.957.957,0,0,1,.449-.346c3.354-1.179,5.933,3.478-1.083,5.322a.458.458,0,0,0,.106-.138" style="fill:#5382a1"></path><path d="M18.8,2s2.909,2.91-2.759,7.386c-4.546,3.59-1.037,5.637,0,7.975-2.653-2.394-4.6-4.5-3.294-6.463C14.664,8.019,19.976,6.623,18.8,2" style="fill:#5382a1"></path><path d="M13.356,29.912c5.042.323,12.786-.179,12.969-2.565,0,0-.353.9-4.167,1.623a41.458,41.458,0,0,1-12.76.2s.645.533,3.959.746" style="fill:#5382a1"></path></g></svg>''',
    "javascript": b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><title>file_type_js</title><path d="M18.774,19.7a3.727,3.727,0,0,0,3.376,2.078c1.418,0,2.324-.709,2.324-1.688,0-1.173-.931-1.589-2.491-2.272l-.856-.367c-2.469-1.052-4.11-2.37-4.11-5.156,0-2.567,1.956-4.52,5.012-4.52A5.058,5.058,0,0,1,26.9,10.52l-2.665,1.711a2.327,2.327,0,0,0-2.2-1.467,1.489,1.489,0,0,0-1.638,1.467c0,1.027.636,1.442,2.1,2.078l.856.366c2.908,1.247,4.549,2.518,4.549,5.376,0,3.081-2.42,4.769-5.671,4.769a6.575,6.575,0,0,1-6.236-3.5ZM6.686,20c.538.954,1.027,1.76,2.2,1.76,1.124,0,1.834-.44,1.834-2.15V7.975h3.422V19.658c0,3.543-2.078,5.156-5.11,5.156A5.312,5.312,0,0,1,3.9,21.688Z" style="fill:black"></path></g></svg>''',
    'c': b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><title>file_type_c3</title><path d="M29,10.232a2.387,2.387,0,0,0-.318-1.244,2.451,2.451,0,0,0-.936-.879Q22.552,5.241,17.353,2.376A2.642,2.642,0,0,0,14.59,2.4c-1.378.779-8.275,4.565-10.331,5.706A2.287,2.287,0,0,0,3,10.231V21.77a2.4,2.4,0,0,0,.3,1.22,2.434,2.434,0,0,0,.954.9c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733a2.444,2.444,0,0,0,.955-.9,2.4,2.4,0,0,0,.3-1.22V10.232" style="fill:#a9b9cb"></path><path d="M28.549,23.171a2.126,2.126,0,0,0,.147-.182,2.4,2.4,0,0,0,.3-1.22V10.232a2.387,2.387,0,0,0-.318-1.244c-.036-.059-.089-.105-.13-.16L16,16Z" style="fill:#8b97a3"></path><path d="M28.549,23.171,16,16,3.451,23.171a2.435,2.435,0,0,0,.809.72c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733A2.43,2.43,0,0,0,28.549,23.171Z" style="fill:#7f8b99"></path><path d="M19.6,18.02a4.121,4.121,0,1,1-.027-4.087l3.615-2.073A8.309,8.309,0,0,0,7.7,16a8.216,8.216,0,0,0,1.1,4.117A8.319,8.319,0,0,0,23.211,20.1L19.6,18.02" style="fill:#fff"></path></g></svg>''',
    'c#': b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><title>file_type_csharp2</title><path d="M29,10.232a2.387,2.387,0,0,0-.318-1.244,2.451,2.451,0,0,0-.936-.879Q22.552,5.241,17.353,2.376A2.642,2.642,0,0,0,14.59,2.4c-1.378.779-8.275,4.565-10.331,5.706A2.287,2.287,0,0,0,3,10.231V21.77a2.4,2.4,0,0,0,.3,1.22,2.434,2.434,0,0,0,.954.9c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733a2.444,2.444,0,0,0,.955-.9,2.4,2.4,0,0,0,.3-1.22V10.232" style="fill:#4e994a"></path><path d="M28.549,23.171a2.126,2.126,0,0,0,.147-.182,2.4,2.4,0,0,0,.3-1.22V10.232a2.387,2.387,0,0,0-.318-1.244c-.036-.059-.089-.105-.13-.16L16,16Z" style="fill:#358230"></path><path d="M28.549,23.171,16,16,3.451,23.171a2.435,2.435,0,0,0,.809.72c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733A2.43,2.43,0,0,0,28.549,23.171Z" style="fill:#1a7515"></path><path d="M19.6,18.02a4.121,4.121,0,1,1-.027-4.087l3.615-2.073A8.309,8.309,0,0,0,7.7,16a8.216,8.216,0,0,0,1.1,4.117A8.319,8.319,0,0,0,23.211,20.1L19.6,18.02" style="fill:#fff"></path><path d="M27.67,15.271V14.033H26.663V13.027H25.424v1.006H23.916V13.027H22.677v1.006H21.669v1.238h1.006v1.513H21.669v1.237h1.006v1.006h1.239V18.021h1.509v1.006h1.239V18.021h1.006V16.784h-1V15.271Zm-2.246,1.513H23.916V15.271h1.508Z" style="fill:#fff"></path></g></svg>''',
    "c++": b'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><title>file_type_cpp3</title><path d="M29,10.232a2.387,2.387,0,0,0-.318-1.244,2.451,2.451,0,0,0-.936-.879Q22.552,5.241,17.353,2.376A2.642,2.642,0,0,0,14.59,2.4c-1.378.779-8.275,4.565-10.331,5.706A2.287,2.287,0,0,0,3,10.231V21.77a2.4,2.4,0,0,0,.3,1.22,2.434,2.434,0,0,0,.954.9c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733a2.444,2.444,0,0,0,.955-.9,2.4,2.4,0,0,0,.3-1.22V10.232" style="fill:#659ad2"></path><path d="M28.549,23.171a2.126,2.126,0,0,0,.147-.182,2.4,2.4,0,0,0,.3-1.22V10.232a2.387,2.387,0,0,0-.318-1.244c-.036-.059-.089-.105-.13-.16L16,16Z" style="fill:#00599c"></path><path d="M28.549,23.171,16,16,3.451,23.171a2.435,2.435,0,0,0,.809.72c2.056,1.141,8.954,4.927,10.332,5.706a2.642,2.642,0,0,0,2.763.026q5.19-2.871,10.386-5.733A2.43,2.43,0,0,0,28.549,23.171Z" style="fill:#004482"></path><path d="M19.6,18.02a4.121,4.121,0,1,1-.027-4.087l3.615-2.073A8.309,8.309,0,0,0,7.7,16a8.216,8.216,0,0,0,1.1,4.117A8.319,8.319,0,0,0,23.211,20.1L19.6,18.02" style="fill:#fff"></path><polygon points="24.076 15.538 23.15 15.538 23.15 14.617 22.225 14.617 22.225 15.538 21.299 15.538 21.299 16.461 22.225 16.461 22.225 17.381 23.15 17.381 23.15 16.461 24.076 16.461 24.076 15.538" style="fill:#fff"></polygon><polygon points="27.549 15.538 26.623 15.538 26.623 14.617 25.697 14.617 25.697 15.538 24.771 15.538 24.771 16.461 25.697 16.461 25.697 17.381 26.623 17.381 26.623 16.461 27.549 16.461 27.549 15.538" style="fill:#fff"></polygon></g></svg>'''
}


def get_icon(language, ax, wmax=64, hmax=64):
    icon_svg = icons[language.lower()]
    svg_mpl_path_iterator = SVGMplPathIterator(icon_svg)
    da = svg_mpl_path_iterator.get_drawing_area(ax, wmax=wmax, hmax=hmax)

    return da

for l, bar in zip(ax.get_yticklabels(), ax.containers[0]):
    language = l.get_text().lower()

    da = get_icon(language, ax, hmax=32)
    ab = AnnotationBbox(da, (1., 0.5), xycoords=bar, frameon=False,
                        xybox=(5, 0), boxcoords="offset points",
                        box_alignment=(0.0, 0.5))
    ax.add_artist(ab)

ax.set_xlim(0, 1.13)

plt.show()
