import sys
            self.processar_pdf(arquivo, 'pagamento')

    def processar_pdf(self, caminho, tipo):
        texto = ''

        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ''

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        convenio = 'bradesco'
        paciente = 'Paciente PDF'
        valor = 500.00
        data = '2026-05-07'

        if tipo == 'producao':
            cursor.execute('''
                INSERT INTO producoes
                (convenio, paciente, tipo, valor, data, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                convenio,
                paciente,
                'consulta',
                valor,
                data,
                'NAO PAGO'
            ))

        else:
            cursor.execute('''
                INSERT INTO pagamentos
                (convenio, paciente, valor, data)
                VALUES (?, ?, ?, ?)
            ''', (
                convenio,
                paciente,
                valor,
                data
            ))

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            'Sucesso',
            'PDF processado com sucesso.'
        )

        self.atualizar_tabelas()

    def atualizar_tabelas(self):
        conn = sqlite3.connect(DB)

        pagos = pd.read_sql_query('SELECT * FROM pagamentos', conn)
        producoes = pd.read_sql_query('SELECT * FROM producoes', conn)

        self.pagos_table.setRowCount(len(pagos))

        for i, row in pagos.iterrows():
            self.pagos_table.setItem(i, 0, QTableWidgetItem(str(row['convenio'])))
            self.pagos_table.setItem(i, 1, QTableWidgetItem(str(row['paciente'])))
            self.pagos_table.setItem(i, 2, QTableWidgetItem(str(row['valor'])))
            self.pagos_table.setItem(i, 3, QTableWidgetItem(str(row['data'])))

        nao_pagos = producoes[producoes['status'] == 'NAO PAGO']

        self.nao_pagos_table.setRowCount(len(nao_pagos))

        for i, row in nao_pagos.iterrows():
            self.nao_pagos_table.setItem(i, 0, QTableWidgetItem(str(row['convenio'])))
            self.nao_pagos_table.setItem(i, 1, QTableWidgetItem(str(row['paciente'])))
            self.nao_pagos_table.setItem(i, 2, QTableWidgetItem(str(row['valor'])))
            self.nao_pagos_table.setItem(i, 3, QTableWidgetItem(str(row['status'])))

        total = pagos['valor'].sum() if not pagos.empty else 0

        self.total_label.setText(f'Total Recebido: R$ {total:.2f}')

        conn.close()

    def gerar_grafico(self):
        conn = sqlite3.connect(DB)

        pagamentos = pd.read_sql_query('''
            SELECT convenio, SUM(valor) as total
            FROM pagamentos
            GROUP BY convenio
        ''', conn)

        self.canvas.ax.clear()

        if not pagamentos.empty:
            self.canvas.ax.bar(
                pagamentos['convenio'],
                pagamentos['total']
            )

            self.canvas.ax.set_title('Ranking de Convênios')
            self.canvas.ax.tick_params(axis='x', rotation=90)

        self.canvas.draw()

        conn.close()


if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')

    create_tables()

    app = QApplication(sys.argv)

    window = MedControl()
    window.show()

    sys.exit(app.exec())