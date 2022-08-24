from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, playlist_name):
        FPDF.__init__(self)
        self.playlist_name = playlist_name
        self.create_pdf()

    def header(self):
        self.set_font('arial', 'B', 20)
        self.cell(0, 10, f"Clustering playlist", 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('arial', 'I', 9)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def description_and_image(self):
        k = 2
        line = 0
        directory = f'clustered{self.playlist_name}/images'
        texts = ['report/correlations.txt', 'report/features.txt', 'report/clusters.txt', 'report/summary.txt']
        images = [f'{directory}/correlation_of_the_features.png',
                  f'{directory}/Features-distribution-across-clusters.png',
                  f'{directory}/Clusters-visualisation.png', '']
        for t, i in zip(texts, images):
            self.ln(line)
            self.set_font('arial', '', 10)
            if i != '':
                f = open(t, 'r')
                for x in f:
                    self.multi_cell(160, 6, txt=x)
                self.image(i, x=None, y=None, w=160, h=120, type='PNG', link='')
                line = 10
            else:
                for num in range(0, k):
                    self.image(f'{directory}/Cluster{num}songs.png', x=None, y=None, w=160, h=120, type='PNG', link='')
                self.set_font('arial', 'B', 12)
                f = open(t, 'r')
                for x in f:
                    self.multi_cell(160, 6, txt=x)

    def title_page(self):
        self.add_page()
        self.image('background-image.png', x=-0.5, y=100, w=self.w+1)
        self.ln(190)
        self.cell(0, 10, "Analysis using Spotify for Developers ", 0, 1, align="C")
    
    def description_page(self):
        self.ln(20)
        self.set_font('arial', '', 10)
        f = open('report/report.txt', 'r')
        for x in f:
            self.multi_cell(160, 6, txt=x)

    def second_page(self):
        self.add_page()
        self.ln(20)
        self.set_font('arial', 'B', 12)
        self.cell(60, 10, "Clustering is grouping of objects based on similarities between them.", ln=1, align='L')
        self.description_page()

    def create_pdf(self):
        self.set_margins(left=25, top=20, right=25)
        self.set_auto_page_break(auto=True, margin=15)

        self.title_page()
        self.second_page()

        self.description_and_image()
        self.output('testing.pdf')
