def get_form_for_user(user, data1, data2):
    numer_mieszkania = user['LOKAL_URZYTKOWY']
    zuzycie_wody_zimnej = round(user["ZUZYCIE_WODY_ZIMNEJ"], 3)
    zuzycie_wody_cieplej = round(user["ZUZYCIE_WODY_CIEPLEJ"], 3)
    stawka_za_wode_zimna = round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)
    stawka_podgrzanie_wody = round(user["STAWKA_ZA_PODGRZANIE_WODY"], 2)
    roznice_licznikow = round(user["ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE"], 2)
    koszt_staly_podgrzania = round(user["KOSZT_STALY_PODGRZANIA"], 2)

    calkowite_zuzycie = round(zuzycie_wody_zimnej + zuzycie_wody_cieplej, 2)
    oplata_zimna_woda = round(stawka_za_wode_zimna * zuzycie_wody_zimnej, 2)
    oplata_ciepla_woda = round(stawka_za_wode_zimna * zuzycie_wody_cieplej, 2)
    oplata_wody = round(oplata_zimna_woda + oplata_ciepla_woda + roznice_licznikow, 2)
    oplata_podgrzanie = round(stawka_podgrzanie_wody * zuzycie_wody_cieplej, 2)
    calkowita_oplata_podgrzanie = round(oplata_podgrzanie + koszt_staly_podgrzania, 2)
    oplata_calkowita = round(calkowita_oplata_podgrzanie + oplata_wody, 2)

    base = f'''
   <html>
      <head>
         <meta content="text/html; charset=UTF-8" http-equiv="content-type">
         <style type="text/css">ol{{margin:0;padding:0}}table td,table th{{padding:0}}.c45{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}}.c35{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}}.c2{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}}.c25{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#f2f2f2;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}}.c21{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}}.c7{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}}.c33{{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}}.c24{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}}.c46{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:39.5pt;border-top-color:#000000;border-bottom-style:solid}}.c16{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:38.2pt;border-top-color:#000000;border-bottom-style:solid}}.c36{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:97pt;border-top-color:#000000;border-bottom-style:solid}}.c42{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:21pt;border-top-color:#000000;border-bottom-style:solid}}.c11{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}}.c41{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}}.c10{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}}.c38{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}}.c39{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:38.2pt;border-top-color:#000000;border-bottom-style:solid}}.c43{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}}.c29{{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}}.c22{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}}.c28{{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:293.2pt;border-top-color:#000000;border-bottom-style:solid}}.c4{{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}}.c0{{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}}.c8{{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left;height:11pt}}.c13{{color:#000000;text-decoration:none;vertical-align:baseline;font-size:10pt;font-family:"Arial";font-style:normal}}.c30{{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left}}.c1{{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:center}}.c44{{text-decoration-skip-ink:none;font-size:10pt;-webkit-text-decoration-skip:none;color:#1155cc;text-decoration:underline}}.c37{{color:#000000;text-decoration:none;vertical-align:baseline;font-family:"Arial";font-style:normal}}.c18{{border-spacing:0;border-collapse:collapse;margin-right:auto}}.c27{{background-color:#ffffff;max-width:451.4pt;padding:72pt 72pt 72pt 72pt}}.c9{{color:inherit;text-decoration:inherit}}.c17{{height:11pt}}.c19{{font-size:12pt}}.c34{{height:17.2pt}}.c5{{height:13.5pt}}.c23{{height:15.8pt}}.c12{{font-size:13pt}}.c31{{height:15pt}}.c26{{font-size:16pt}}.c32{{height:32.2pt}}.c14{{color:#ff0000}}.c20{{height:27pt}}.c15{{font-weight:400}}.c3{{font-size:9pt}}.c40{{height:22pt}}.c6{{font-weight:700}}.title{{padding-top:0pt;color:#000000;font-size:26pt;padding-bottom:3pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}.subtitle{{padding-top:0pt;color:#666666;font-size:15pt;padding-bottom:16pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}li{{color:#000000;font-size:11pt;font-family:"Arial"}}p{{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}}h1{{padding-top:20pt;color:#000000;font-size:20pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}h2{{padding-top:18pt;color:#000000;font-size:16pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}h3{{padding-top:16pt;color:#434343;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}h4{{padding-top:14pt;color:#666666;font-size:12pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}h5{{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}}h6{{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}}</style>
      </head>
      <body class="c27 doc-content">
         <p class="c1"><span class="c13 c6">Wsp&oacute;lnota Mieszkaniowa Nieruchomo&#347;ci przy ul. Misjonarskiej 1b w P&#322;ocku</span></p>
         <p class="c1 c17"><span class="c13 c6"></span></p>
         <p class="c30"><span class="c13 c15">ul. Misjonarska 1B </span></p>
         <p class="c30"><span class="c13 c15">09-402 P&#322;ock</span></p>
         <p class="c30"><span class="c44"><a class="c9" href="mailto:wspolnota.misjonarska@gmail.com">wspolnota.misjonarska@gmail.com</a></span></p>
         <p class="c8"><span class="c13 c15"></span></p>
         <p class="c8"><span class="c19 c6 c37"></span></p>
         <p class="c1"><span class="c19 c6">Rozliczenie op&#322;at za wod&#281; za okres od {data1} do {data2} roku</span></p>
         <p class="c8"><span class="c6 c13"></span></p>
         <p class="c30"><span class="c0">Mieszkanie nr: {numer_mieszkania}</span></p>
         <p class="c8"><span class="c0"></span></p>
         <hr>
         <p class="c8"><span class="c0"></span></p>
         <p class="c8"><span class="c0"></span></p>
         <p class="c1"><span class="c0">Op&#322;aty</span></p>
         <p class="c1 c17"><span class="c0"></span></p>
         <a id="t.fe448e50505a54ebfb8559fe71fc9a2a29a31d97"></a><a id="t.0"></a>
         <table class="c18">
            <tr class="c32">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">WODA</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">[m3]</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Stawka [z&#322;/m3]</span></p>
               </td>
               <td class="c35" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[a]</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[b]</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[a]x[b]</span></p>
               </td>
            </tr>
            <tr class="c31">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">Koszt zuzycia zimnej wody</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">[1]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{zuzycie_wody_zimnej}</span></p>
               </td>
               <td class="c25" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{stawka_za_wode_zimna} z&#322;</span></p>
               </td>
               <td class="c35" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{oplata_zimna_woda} z&#322;</span></p>
               </td>
            </tr>
            <tr class="c23">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">Koszt zu&#380;ycia ciep&#322;ej wody</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">[2]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{zuzycie_wody_cieplej}</span></p>
               </td>
               <td class="c25" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{stawka_za_wode_zimna} z&#322;</span></p>
               </td>
               <td class="c35" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{oplata_ciepla_woda} z&#322;</span></p>
               </td>
            </tr>
            <tr class="c23">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">R&oacute;&#380;nice licznikowe</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">[3]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c25" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c14">{roznice_licznikow} z&#322;</span></p>
               </td>
            </tr>
            <tr class="c23">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Razem [1]+[2]</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">[4]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">{calkowite_zuzycie}</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">{stawka_za_wode_zimna} z&#322;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">{oplata_wody} z&#322;</span></p>
               </td>
            </tr>
         </table>
         <p class="c1 c17"><span class="c0"></span></p>
         <a id="t.09de1ba7de720b02179c271bb08b0abcd1665102"></a><a id="t.1"></a>
         <table class="c18">
            <tr class="c32">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">PODGRZANIE</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">[m3]</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Stawka [z&#322;/m3]</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[a]</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[b]</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">[a]x[b]</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">Koszt ogrzania wody</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">[5]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{zuzycie_wody_cieplej}</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{stawka_podgrzanie_wody} z&#322;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{oplata_podgrzanie} z&#322;</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
            </tr>
            <tr class="c20">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                   <p class="c1"><span class="c0">Kwota</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">ilo&#347;&#263; miesi&#281;cy</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">Koszt sta&#322;y podgrzania wody</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">[6]</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{koszt_staly_podgrzania} z&#322</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">1</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{koszt_staly_podgrzania} z&#322</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">&nbsp;</span></p>
               </td>
            </tr>
            <tr class="c5">
               <td class="c11" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c10" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3 c6">&nbsp;</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3 c6">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3 c6">&nbsp;</span></p>
               </td>
            </tr>
            <tr class="c31">
               <td class="c22" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c39" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c43" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c24" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
               <td class="c45" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">&nbsp;</span></p>
               </td>
            </tr>
            <tr class="c34">
               <td class="c21" colspan="1" rowspan="1">
                  <p class="c1"><span class="c19 c6">Razem &nbsp;podgrzanie</span></p>
               </td>
               <td class="c16" colspan="1" rowspan="1">
                  <p class="c1"><span class="c6 c19">[7]</span></p>
               </td>
               <td class="c38" colspan="1" rowspan="1">
                  <p class="c1"><span class="c19 c6">&nbsp;</span></p>
               </td>
               <td class="c41" colspan="1" rowspan="1">
                  <p class="c1"><span class="c19 c6">&nbsp;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c19 c6">{calkowita_oplata_podgrzanie} z&#322;</span></p>
               </td>
            </tr>
         </table>
         <p class="c1 c17"><span class="c0"></span></p>
         <a id="t.eb93e17c290906fe80293081e7c6b588eb5cd113"></a><a id="t.2"></a>
         <table class="c18">
            <tr class="c40">
               <td class="c28" colspan="3" rowspan="1">
                  <p class="c1"><span class="c6 c12">Saldo na dzie&#324; {data2}: [7]+[4] &nbsp; &nbsp; &nbsp; </span><span class="c26 c6">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </span></p>
               </td>
               <td class="c42" colspan="1" rowspan="1">
                  <p class="c30"><span class="c26 c6">&nbsp;</span></p>
               </td>
               <td class="c36" colspan="1" rowspan="1">
                  <p class="c1"><span class="c6 c26">{oplata_calkowita} z&#322;</span></p>
               </td>
               <td class="c46" colspan="1" rowspan="1">
                  <p class="c30"><span class="c26 c6">&nbsp;</span></p>
               </td>
            </tr>
         </table>
         <p class="c1 c17"><span class="c0"></span></p>
         <p class="c1 c17"><span class="c0"></span></p>
         <hr>
         <p class="c1 c17"><span class="c0"></span></p>
         <p class="c1 c17"><span class="c0"></span></p>
      </body>
   </html>
   '''
    return base


def get_form_user_formal(user, data1, data2, aktualna_data):
    rachunek_bankowy = str(user["RACHUNEK_BANKOWY"])
    sprzedawca = user["SPRZEDAWCA"]
    adres_korespondacyjny = str(user["ADRES_KORESPONDENCYJNY"])
    nabywca = str(user["NABYWCA"])

    numer_mieszkania = user['LOKAL_URZYTKOWY']
    zuzycie_wody_zimnej = round(user["ZUZYCIE_WODY_ZIMNEJ"], 3)
    zuzycie_wody_cieplej = round(user["ZUZYCIE_WODY_CIEPLEJ"], 3)
    stawka_za_wode_zimna = round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)
    stawka_podgrzanie_wody = round(user["STAWKA_ZA_PODGRZANIE_WODY"], 2)
    roznice_licznikow = round(user["ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE"], 2)
    koszt_staly_podgrzania = round(user["KOSZT_STALY_PODGRZANIA"], 2)

    calkowite_zuzycie = round(zuzycie_wody_zimnej + zuzycie_wody_cieplej, 2)
    oplata_zimna_woda = round(stawka_za_wode_zimna * zuzycie_wody_zimnej, 2)
    oplata_ciepla_woda = round(stawka_za_wode_zimna * zuzycie_wody_cieplej, 2)
    oplata_wody = round(oplata_zimna_woda + oplata_ciepla_woda + roznice_licznikow, 2)
    oplata_podgrzanie = round(stawka_podgrzanie_wody * zuzycie_wody_cieplej, 2)
    calkowita_oplata_podgrzanie = round(oplata_podgrzanie + koszt_staly_podgrzania, 2)
    oplata_calkowita = round(calkowita_oplata_podgrzanie + oplata_wody, 2)

    # preprocessing
    raw = nabywca.split('|')
    nabywca = ""
    for line in raw:
        nabywca += f'<p class ="c23"> <span class="c18">{line}</span></p>\n'

    raw = adres_korespondacyjny.split('|')
    adres_korespondacyjny = ""
    for line in raw:
        adres_korespondacyjny += f'<p class ="c23"><span class ="c18">{line}</span></p>\n'

    base = '''
   <html>
   <head>
      <meta content="text/html; charset=UTF-8" http-equiv="content-type">
      <style type="text/css">ol{margin:0;padding:0}table td,table th{padding:0}.c26{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}.c8{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:38.2pt;border-top-color:#000000;border-bottom-style:solid}.c54{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:38.2pt;border-top-color:#000000;border-bottom-style:solid}.c2{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}.c0{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}.c50{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}.c52{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:21pt;border-top-color:#000000;border-bottom-style:solid}.c45{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:97pt;border-top-color:#000000;border-bottom-style:solid}.c5{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}.c22{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}.c25{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}.c55{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:293.2pt;border-top-color:#000000;border-bottom-style:solid}.c19{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:50.3pt;border-top-color:#000000;border-bottom-style:solid}.c36{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:162.3pt;border-top-color:#000000;border-bottom-style:solid}.c11{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}.c15{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}.c30{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#f2f2f2;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}.c57{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:186pt;border-top-color:#000000;border-bottom-style:solid}.c56{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}.c24{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}.c49{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:70.7pt;border-top-color:#000000;border-bottom-style:solid}.c53{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:39.5pt;border-top-color:#000000;border-bottom-style:solid}.c37{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:0pt;border-right-width:0pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;border-left-style:solid;border-bottom-width:0pt;width:225.7pt;border-top-color:#000000;border-bottom-style:solid}.c7{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:9pt;font-family:"Arial";font-style:normal}.c1{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:10pt;font-family:"Arial";font-style:normal}.c18{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:7pt;font-family:"Arial";font-style:normal}.c13{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:9pt;font-family:"Arial";font-style:normal}.c3{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left;height:11pt}.c10{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:12pt;font-family:"Arial";font-style:normal}.c9{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:10pt;font-family:"Arial";font-style:normal}.c48{padding-top:12pt;padding-bottom:12pt;line-height:1.15;orphans:2;widows:2;text-align:center}.c32{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:right}.c31{color:#000000;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c20{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c4{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:center}.c34{color:#000000;text-decoration:none;vertical-align:baseline;font-family:"Arial";font-style:normal}.c46{margin-left:auto;border-spacing:0;border-collapse:collapse;margin-right:auto}.c29{border-spacing:0;border-collapse:collapse;margin-right:auto}.c23{padding-top:0pt;padding-bottom:0pt;line-height:1.0;text-align:left}.c47{background-color:#ffffff;max-width:451.4pt;padding:72pt 72pt 72pt 72pt}.c42{height:32.2pt}.c41{font-size:14pt}.c12{font-size:8pt}.c17{height:0pt}.c14{font-weight:700}.c33{font-size:9pt}.c51{font-weight:400}.c16{height:27pt}.c21{height:13.5pt}.c39{height:15.8pt}.c44{font-size:12pt}.c38{height:15pt}.c35{font-size:15pt}.c6{height:11pt}.c28{color:#ff0000}.c27{font-size:10pt}.c43{height:22pt}.c40{height:17.2pt}.title{padding-top:0pt;color:#000000;font-size:26pt;padding-bottom:3pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}.subtitle{padding-top:0pt;color:#666666;font-size:15pt;padding-bottom:16pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}li{color:#000000;font-size:11pt;font-family:"Arial"}p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}h1{padding-top:20pt;color:#000000;font-size:20pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h2{padding-top:18pt;color:#000000;font-size:16pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h3{padding-top:16pt;color:#434343;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h4{padding-top:14pt;color:#666666;font-size:12pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h5{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h6{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}</style>
   </head>
   ''' + f'''
   <body class="c47 doc-content">
      <p class="c32"><span class="c27">P&#322;ock, dnia {aktualna_data}</span></p>
      <p class="c20"><span class="c14 c41">ZAWIADOMIENIE O WYSOKOS&#769;CI OP&#321;AT</span></p>
      <p class="c4"><span class="c1">ORYGINA&#321;</span></p>
      <p class="c4 c6"><span class="c1"></span></p>
      <a id="t.f0d9fc78573dcc27877940b69c380dbbfcac685e"></a><a id="t.0"></a>
      <table class="c46">
         <tr class="c17">
            <td class="c37" colspan="1" rowspan="1">
               <p class="c20"><span class="c7">SPRZEDAWCA</span></p>
               <a id="t.425f73ee1e6e70fdb7e36eb9efc5f1c4fb7d73e9"></a><a id="t.1"></a>
               <table class="c29">
                  <tr class="c17">
                     <td class="c57" colspan="1" rowspan="1">
                        <p class="c23"><span class="c7">WSPO&#769;LNOTA MIESZKANIOWA</span></p>
                        <p class="c23"><span class="c7">MISJONARSKA 1B</span></p>
                        <p class="c23"><span class="c13">ul. Misjonarska 1b</span></p>
                        <p class="c23"><span class="c33">09-402 P&#322;ock</span><span class="c18">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                        <p class="c23"><span class="c33">NIP: </span><span class="c12">774-321-13-47 </span></p>
                     </td>
                  </tr>
               </table>
               <p class="c3"><span class="c7"></span></p>
            </td>
            <td class="c37" colspan="1" rowspan="1">
               <p class="c20"><span class="c14 c33">NABYWCA</span><span class="c33">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
               <a id="t.fa220273a449114b2812822406f2f30750fe30ca"></a><a id="t.2"></a>
               <table class="c29">
                  <tr class="c17">
                     <td class="c57" colspan="1" rowspan="1">
                        {nabywca}
                        <p class="c23"><span class="c13"></span></p>
                        <p class="c23"><span class="c7">Adres korespondencyjny:</span></p>
                        {adres_korespondacyjny}
                     </td>
                  </tr>
               </table>
               <p class="c3"><span class="c7"></span></p>
            </td>
         </tr>
      </table>
      <p class="c20"><span class="c7">RACHUNEK BANKOWY:</span></p>
      <p class="c20"><span class="c14 c33">{rachunek_bankowy}</span><span class="c1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c48"><span class="c13">dotyczy zuz&#775;ycia wody w lokalu us&#322;ugowym: Misjonarska 1B (09-402 P&#322;ock) </span></p>
      <hr>
      <p class="c3"><span class="c13"></span></p>
      <p class="c4"><span class="c14 c27">Rozliczenie op&#322;at za wod&#281; za okres od {data1} do {data2} roku</span></p>
      <p class="c3"><span class="c34 c12 c14"></span></p>
      <p class="c20"><span class="c14 c33">Mieszkanie nr: {numer_mieszkania}</span></p>
      <p class="c4"><span class="c1">Op&#322;aty</span></p>
      <p class="c4 c6"><span class="c1"></span></p>
      <a id="t.fe448e50505a54ebfb8559fe71fc9a2a29a31d97"></a><a id="t.3"></a>
      <table class="c29">
         <tr class="c42">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">WODA</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">[m3]</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Stawka [z&#322;/m3]</span></p>
            </td>
            <td class="c36" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
            </td>
         </tr>
         <tr class="c21">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[a]</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[b]</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[a]x[b]</span></p>
            </td>
         </tr>
         <tr class="c38">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">Koszt zuzycia zimnej wody</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">[1]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">{zuzycie_wody_zimnej}</span></p>
            </td>
            <td class="c30" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">{stawka_za_wode_zimna} z&#322;</span></p>
            </td>
            <td class="c36" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">{oplata_zimna_woda} z&#322;</span></p>
            </td>
         </tr>
         <tr class="c39">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">Koszt zu&#380;ycia ciep&#322;ej wody</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">[2]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">{zuzycie_wody_cieplej}</span></p>
            </td>
            <td class="c30" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">{stawka_za_wode_zimna} z&#322;</span></p>
            </td>
            <td class="c36" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">115.93 z&#322;</span></p>
            </td>
         </tr>
         <tr class="c39">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">R&oacute;&#380;nice licznikowe</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">[3]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c30" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c27 c28">{roznice_licznikow} z&#322;</span></p>
            </td>
         </tr>
         <tr class="c39">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Razem [1]+[2]</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">[4]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">{calkowite_zuzycie}</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">{stawka_za_wode_zimna} z&#322;</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">{oplata_wody} z&#322;</span></p>
            </td>
         </tr>
      </table>
      <p class="c4 c6"><span class="c1"></span></p>
      <a id="t.3ac2a84acdeaedde4e7ef97d1ce252a1458e6f61"></a><a id="t.4"></a>
      <table class="c29">
         <tr class="c42">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">PODGRZANIE</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">[m3]</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Stawka [z&#322;/m3]</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
            </td>
         </tr>
         <tr class="c21">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[a]</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[b]</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">[a]x[b]</span></p>
            </td>
         </tr>
         <tr class="c21">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">Koszt ogrzania wody</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">[5]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">{zuzycie_wody_cieplej}</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">{stawka_podgrzanie_wody}</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">{oplata_podgrzanie}</span></p>
            </td>
         </tr>
         <tr class="c21">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">&nbsp;</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">&nbsp;</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">&nbsp;</span></p>
            </td>
         </tr>
         <tr class="c16">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">&nbsp;</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">Kwota </span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">ilo&#347;&#263; miesi&#281;cy</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
            </td>
         </tr>
         <tr class="c21">
            <td class="c0" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">Koszt sta&#322;y podgrzania wody</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c9">[6]</span></p>
            </td>
            <td class="c2" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">{koszt_staly_podgrzania}</span></p>
            </td>
            <td class="c11" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">1</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c12">{koszt_staly_podgrzania}</span></p>
            </td>
         </tr>
         <tr class="c38">
            <td class="c50" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c54" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c19" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c56" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
            <td class="c22" colspan="1" rowspan="1">
               <p class="c4"><span class="c1">&nbsp;</span></p>
            </td>
         </tr>
         <tr class="c40">
            <td class="c25" colspan="1" rowspan="1">
               <p class="c4"><span class="c14">Razem &nbsp;podgrzanie</span></p>
            </td>
            <td class="c8" colspan="1" rowspan="1">
               <p class="c4"><span class="c14">[7]</span></p>
            </td>
            <td class="c26" colspan="1" rowspan="1">
               <p class="c4"><span class="c14">&nbsp;</span></p>
            </td>
            <td class="c49" colspan="1" rowspan="1">
               <p class="c4"><span class="c14">&nbsp;</span></p>
            </td>
            <td class="c5" colspan="1" rowspan="1">
               <p class="c4"><span class="c14">{calkowita_oplata_podgrzanie} z&#322;</span></p>
            </td>
         </tr>
      </table>
      <p class="c4 c6"><span class="c1"></span></p>
      <a id="t.eb93e17c290906fe80293081e7c6b588eb5cd113"></a><a id="t.5"></a>
      <table class="c29">
         <tr class="c43">
            <td class="c55" colspan="3" rowspan="1">
               <p class="c4"><span class="c14 c44">Saldo na dzie&#324; {data2}: [7]+[4] &nbsp; &nbsp; &nbsp; </span><span class="c14 c35">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </span></p>
            </td>
            <td class="c52" colspan="1" rowspan="1">
               <p class="c20"><span class="c14 c35">&nbsp;</span></p>
            </td>
            <td class="c45" colspan="1" rowspan="1">
               <p class="c4"><span class="c14 c35">{oplata_calkowita} z&#322;</span></p>
            </td>
            <td class="c53" colspan="1" rowspan="1">
               <p class="c20"><span class="c14 c35">&nbsp;</span></p>
            </td>
         </tr>
      </table>
      <p class="c3"><span class="c31 c14"></span></p>
      <hr>
      <p class="c4 c6"><span class="c31 c14"></span></p>
      <p class="c4 c6"><span class="c10"></span></p>
      <p class="c4"><span class="c10">Op&#322;aty nalez&#775;y wnosic&#769; na konto bankowe w terminie 7 dni od daty wystawienia zawiadomienia. </span></p>
      <p class="c4"><span class="c31 c14">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c4"><span class="c31 c14">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c4"><span class="c14 c31">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c4 c6"><span class="c31 c14"></span></p>
   </body>
</html>
   '''
    return base
def get_form_user_electricy(user, data1, data2, aktualna_data):
    rachunek_bankowy = str(user["RACHUNEK_BANKOWY"])
    print(user)

    numer_mieszkania = user['LOKAL_URZYTKOWY']
    zuzycie_kwh= round(user["ZUZYCIE_KWH"], 2)
    stawka_kwh = round(user["STAWKA_KWH"], 2)

    koszt_staly = round(5.001, 2)
    koszt_czesciowy = round(zuzycie_kwh * stawka_kwh, 2)
    koszt_calkowity = round(koszt_staly + koszt_czesciowy, 2)


    base = '''
   <html>
   <head>
      <meta content="text/html; charset=UTF-8" http-equiv="content-type">
      <style type="text/css">ol{margin:0;padding:0}table td,table th{padding:0}.c4{border-right-style:solid;padding:1pt 1pt 5pt 1pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:57pt;border-top-color:#000000;border-bottom-style:solid}.c6{border-right-style:solid;padding:1pt 1pt 5pt 1pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}.c40{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:39.5pt;border-top-color:#000000;border-bottom-style:solid}.c26{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:0pt;border-right-width:0pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;border-left-style:solid;border-bottom-width:0pt;width:225.7pt;border-top-color:#000000;border-bottom-style:solid}.c44{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:293.2pt;border-top-color:#000000;border-bottom-style:solid}.c42{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:21pt;border-top-color:#000000;border-bottom-style:solid}.c41{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}.c22{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:186pt;border-top-color:#000000;border-bottom-style:solid}.c10{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;background-color:#ffffff;border-left-style:solid;border-bottom-width:1pt;width:30.8pt;border-top-color:#000000;border-bottom-style:solid}.c27{border-right-style:solid;padding:5pt 5pt 5pt 5pt;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:top;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:5.2pt;border-top-color:#000000;border-bottom-style:solid}.c43{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:0pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:0pt;border-top-style:solid;background-color:#a6a6a6;border-left-style:solid;border-bottom-width:1pt;width:97pt;border-top-color:#000000;border-bottom-style:solid}.c28{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:57pt;border-top-color:#000000;border-bottom-style:solid}.c24{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:129.8pt;border-top-color:#000000;border-bottom-style:solid}.c30{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:162pt;border-top-color:#000000;border-bottom-style:solid}.c3{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:middle;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:71.2pt;border-top-color:#000000;border-bottom-style:solid}.c16{border-right-style:solid;border-bottom-color:#000000;border-top-width:1pt;border-right-width:1pt;border-left-color:#000000;vertical-align:bottom;border-right-color:#000000;border-left-width:1pt;border-top-style:solid;border-left-style:solid;border-bottom-width:1pt;width:162pt;border-top-color:#000000;border-bottom-style:solid}.c15{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c8{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:9pt;font-family:"Arial";font-style:normal}.c7{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:10pt;font-family:"Arial";font-style:normal}.c5{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:10pt;font-family:"Arial";font-style:normal}.c45{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:right}.c1{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:center}.c0{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c29{padding-top:12pt;padding-bottom:12pt;line-height:1.15;orphans:2;widows:2;text-align:center}.c32{color:#000000;text-decoration:none;vertical-align:baseline;font-family:"Arial";font-style:normal}.c48{margin-left:auto;border-spacing:0;border-collapse:collapse;margin-right:auto}.c19{border-spacing:0;border-collapse:collapse;margin-right:auto}.c18{padding-top:0pt;padding-bottom:0pt;line-height:1.0;text-align:left}.c39{font-weight:400;font-size:7pt}.c2{font-size:15pt;font-weight:700}.c17{font-size:12pt;font-weight:700}.c47{max-width:451.4pt;padding:72pt 72pt 72pt 72pt}.c46{font-weight:400;font-size:14pt}.c21{font-size:9pt;font-weight:700}.c23{font-size:14pt;font-weight:700}.c38{font-weight:400;font-size:11pt}.c25{font-weight:700}.c13{height:15pt}.c34{font-size:9pt}.c33{padding:1pt 1pt 5pt 1pt}.c14{height:15.8pt}.c37{height:13.5pt}.c11{background-color:#ffffff}.c12{height:11pt}.c35{height:22pt}.c36{height:32.2pt}.c9{height:0pt}.c31{font-size:10pt}.c20{font-size:8pt}.title{padding-top:0pt;color:#000000;font-size:26pt;padding-bottom:3pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}.subtitle{padding-top:0pt;color:#666666;font-size:15pt;padding-bottom:16pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}li{color:#000000;font-size:11pt;font-family:"Arial"}p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}h1{padding-top:20pt;color:#000000;font-size:20pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h2{padding-top:18pt;color:#000000;font-size:16pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h3{padding-top:16pt;color:#434343;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h4{padding-top:14pt;color:#666666;font-size:12pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h5{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h6{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}</style>
   </head>
   ''' + f'''
   <body class="c11 c47 doc-content">
      <p class="c45"><span class="c31">P&#322;ock, dnia {aktualna_data}</span></p>
      <p class="c0"><span class="c23">ZAWIADOMIENIE O WYSOKOS&#769;CI OP&#321;AT</span></p>
      <p class="c1"><span class="c7">ORYGINA&#321;</span></p>
      <p class="c1 c12"><span class="c7"></span></p>
      <table class="c48">
         <tr class="c9">
            <td class="c26" colspan="1" rowspan="1">
               <p class="c0"><span class="c32 c21">SPRZEDAWCA</span></p>
               <table class="c19">
                  <tr class="c9">
                     <td class="c22" colspan="1" rowspan="1">
                        <p class="c18"><span class="c32 c21">WSPO&#769;LNOTA MIESZKANIOWA</span></p>
                        <p class="c18"><span class="c32 c21">MISJONARSKA 1B</span></p>
                        <p class="c18"><span class="c8">ul. Misjonarska 1b</span></p>
                        <p class="c18"><span class="c34">09-402 P&#322;ock</span><span class="c32 c39">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
                        <p class="c18"><span class="c34">NIP: </span><span class="c20">774-321-13-47 </span></p>
                     </td>
                  </tr>
               </table>
               <p class="c0 c12"><span class="c32 c21"></span></p>
            </td>
            <td class="c26" colspan="1" rowspan="1">
               <p class="c0 c12"><span class="c32 c21"></span></p>
            </td>
         </tr>
      </table>
      <p class="c0"><span class="c32 c21">RACHUNEK BANKOWY:</span></p>
      <p class="c0"><span class="c21">{rachunek_bankowy}</span><span class="c7">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c12 c29"><span class="c8"></span></p>
      <hr>
      <p class="c0 c12"><span class="c8"></span></p>
      <p class="c1"><span class="c25 c31">Rozliczenie op&#322;at za energi&#281; elektryczn&#261; za okres od {data1} do {data2} roku</span></p>
      <p class="c0 c12"><span class="c32 c25 c20"></span></p>
      <p class="c0"><span class="c21">Mieszkanie nr: {numer_mieszkania}</span></p>
      <p class="c1"><span class="c7">Op&#322;aty</span></p>
      <p class="c1 c12"><span class="c7"></span></p>
      <table class="c19">
         <tr class="c36">
            <td class="c6" colspan="1" rowspan="1">
               <p class="c1"><span class="c25">Energia elektryczna</span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">&nbsp;</span></p>
            </td>
            <td class="c28 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">kWh</span></p>
            </td>
            <td class="c3 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">Stawka [z&#322;/kWh]</span></p>
            </td>
            <td class="c16 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">Kwota obci&#261;&#380;enia mieszkania za ca&#322;y okres</span></p>
            </td>
         </tr>
         <tr class="c37">
            <td class="c24 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">&nbsp;</span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">&nbsp;</span></p>
            </td>
            <td class="c28 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c20">[a]</span></p>
            </td>
            <td class="c3 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c20">[b]</span></p>
            </td>
            <td class="c30 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c20">[a]x[b]</span></p>
            </td>
         </tr>
         <tr class="c13">
            <td class="c24 c33 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">Koszt energii elektrycznej</span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">[1]</span></p>
            </td>
            <td class="c4" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">{zuzycie_kwh}</span></p>
            </td>
            <td class="c3 c33" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">{stawka_kwh} z&#322;</span></p>
            </td>
            <td class="c16 c11 c33" colspan="1" rowspan="1">
               <p class="c1"><span class="c31">{koszt_czesciowy} z&#322;</span></p>
            </td>
         </tr>
         <tr class="c14">
            <td class="c24 c33 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">Op&#322;ata manipulacyjna</span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">[2]</span></p>
            </td>
            <td class="c28 c11" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c5"></span></p>
            </td>
            <td class="c3" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c5"></span></p>
            </td>
            <td class="c11 c16" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">{koszt_staly} z&#322;</span></p>
            </td>
         </tr>
         <tr class="c14">
            <td class="c24 c11" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c5"></span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c5"></span></p>
            </td>
            <td class="c11 c28" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">&nbsp;</span></p>
            </td>
            <td class="c3" colspan="1" rowspan="1">
               <p class="c1"><span class="c5">&nbsp;</span></p>
            </td>
            <td class="c11 c30" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c5"></span></p>
            </td>
         </tr>
         <tr class="c14">
            <td class="c11 c24" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">Razem [1]+[2]</span></p>
            </td>
            <td class="c10" colspan="1" rowspan="1">
               <p class="c1"><span class="c7">[3]</span></p>
            </td>
            <td class="c28 c11" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c7"></span></p>
            </td>
            <td class="c3" colspan="1" rowspan="1">
               <p class="c1 c12"><span class="c7"></span></p>
            </td>
            <td class="c30 c33 c11" colspan="1" rowspan="1">
               <p class="c1"><span class="c25">{koszt_calkowity} z&#322;</span></p>
            </td>
         </tr>
      </table>
      <p class="c1 c12"><span class="c7"></span></p>
      <table class="c19">
         <tr class="c35">
            <td class="c44" colspan="3" rowspan="1">
               <p class="c1"><span class="c17">Saldo na dzie&#324; {data2}: [3] &nbsp; &nbsp; &nbsp; </span><span class="c2">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </span></p>
            </td>
            <td class="c42" colspan="1" rowspan="1">
               <p class="c0"><span class="c2">&nbsp;</span></p>
            </td>
            <td class="c43" colspan="1" rowspan="1">
               <p class="c1"><span class="c2">{koszt_calkowity} z&#322;</span></p>
            </td>
            <td class="c40" colspan="1" rowspan="1">
               <p class="c0"><span class="c2">&nbsp;</span></p>
            </td>
         </tr>
      </table>
      <p class="c0 c12"><span class="c15"></span></p>
      <hr>
      <p class="c1 c12"><span class="c15"></span></p>
      <p class="c1 c12"><span class="c32 c17"></span></p>
      <p class="c1 c12"><span class="c15"></span></p>
      <p class="c1"><span class="c15">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c1"><span class="c15">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>
      <p class="c1 c12"><span class="c15"></span></p>
      <p class="c0 c12"><span class="c32 c38"></span></p>
   </body>
</html>
   '''
    return base
