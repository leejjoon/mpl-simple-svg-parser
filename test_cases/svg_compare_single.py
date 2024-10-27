from svg_renderer_helper import compare_svg_result

import matplotlib.pyplot as plt
fig = plt.figure(1, figsize=(8, 2.3))
fig.clf()
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.05, hspace=0.05, wspace=0.05)
fig.patch.set_fc("gold")

fn = "w3_svg_samples/python.svg"
fn = "w3_svg_samples/gallardo_no_unit.svg"
fn = "w3_svg_samples/twitter.svg"
fn = "w3_svg_samples/php.svg"
fn = "w3_svg_samples/rg1024_metal_effect.svg"
fn = "w3_svg_samples/svg2009.svg"
fn = "w3_svg_samples/twitter.svg"
fn = "w3_svg_samples/ca.svg"
compare_svg_result(fig, fn)
plt.show()

# gallardo
