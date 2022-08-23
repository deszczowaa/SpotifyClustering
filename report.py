from fpdf import FPDF

playlist_name = "Level22"

k = 2


class PDF(FPDF):
    def header(self):
        self.set_font('arial', 'B', 20)
        self.cell(0, 10, f"Clustering {playlist_name} playlist", 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('arial', 'I', 9)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


# create pdf
pdf = PDF()
pdf.set_margins(left=25, top=20, right=25)
pdf.set_auto_page_break(auto=True, margin=15)

# add title page
pdf.add_page()
pdf.image('report/background-image.png', x=-0.5, y=100, w=pdf.w+1)
pdf.set_font('arial', 'I', 14)
pdf.ln(190)
pdf.cell(0, 10, "Analysis using Spotify for Developers ", 0, 1, align="C")

# add other pages
pdf.add_page()
pdf.set_xy(0, 0)
pdf.ln(40)
pdf.set_font('arial', 'B', 12)
pdf.cell(60, 10, "Clustering is grouping of objects based on similarities between them.", ln=1, align='L')
f = open('report/report.txt', 'r')
pdf.set_font('arial', '', 10)
for x in f:
    pdf.multi_cell(160, 6, txt=x)

pdf.add_page()
pdf.ln(10)
pdf.set_font('arial', '', 10)
f = open('report/correlations.txt', 'r')
for x in f:
    pdf.multi_cell(160, 6, txt=x)
pdf.image(f'clustered{playlist_name}/images/correlation_of_the_features.png', x = None, y = None, w = 160, h = 120, type = '', link = '')
pdf.add_page()
pdf.ln(10)
f = open('report/features.txt', 'r')
pdf.set_font('arial', '', 10)
for x in f:
    pdf.multi_cell(160, 6, txt=x)
pdf.image(f'clustered{playlist_name}/images/Features-distribution-across-clusters.png', x = None, y = None, w = 160, h = 120, type = '', link = '')

pdf.ln(10)
f = open('report/clusters.txt', 'r')
pdf.set_font('arial', '', 10)
for x in f:
    pdf.multi_cell(160, 6, txt=x)
pdf.image(f'clustered{playlist_name}/images/Clusters-visualisation.png', x = None, y = None, w = 160, h = 120, type = '', link = '')
for num in range(0, k):
    pdf.image(f'clustered{playlist_name}/images/Cluster{num}songs.png', x = None, y = None, w = 160, h = 120, type = '', link = '')
pdf.ln(10)
f = open('report/summary.txt', 'r')
pdf.set_font('arial', 'B', 12)
for x in f:
    pdf.multi_cell(160, 6, txt=x)

pdf.output('Clustering-report.pdf', 'F')
