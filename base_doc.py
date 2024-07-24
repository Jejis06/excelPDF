
def get_form_for_user(user):

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
         <p class="c1"><span class="c19 c6">Rozliczenie op&#322;at za wod&#281; za okres od {"data1"} do {"data2"} roku</span></p>
         <p class="c8"><span class="c6 c13"></span></p>
         <p class="c30"><span class="c0">Mieszkanie nr: {user["LOKAL_URZYTKOWY"]}</span></p>
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
                  <p class="c1"><span class="c4">{round(user["ZUZYCIE_WODY_ZIMNEJ"], 2)}</span></p>
               </td>
               <td class="c25" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)} z&#322;</span></p>
               </td>
               <td class="c35" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"] * user["ZUZYCIE_WODY_ZIMNEJ"], 2) } z&#322;</span></p>
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
                  <p class="c1"><span class="c4">{round(user["ZUZYCIE_WODY_CIEPLEJ"], 2)}</span></p>
               </td>
               <td class="c25" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)} z&#322;</span></p>
               </td>
               <td class="c35" colspan="1" rowspan="1">
                  <p class="c1"><span class="c4">{round(user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)} z&#322;</span></p>
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
                  <p class="c1"><span class="c14">{round(user["ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE"], 2)} z&#322;</span></p>
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
                  <p class="c1"><span class="c0">{round(user["ZUZYCIE_WODY_ZIMNEJ"] + user["ZUZYCIE_WODY_CIEPLEJ"], 2)}</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">{round(user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"], 2)} z&#322;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c0">{round(user["ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE"] + user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"] + user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"] * user["ZUZYCIE_WODY_ZIMNEJ"], 2)} z&#322;</span></p>
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
                  <p class="c1"><span class="c3">{round(user["ZUZYCIE_WODY_CIEPLEJ"], 2)}</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{round(user["STAWKA_ZA_PODGRZANIE_WODY"], 2)} z&#322;</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{round(user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_PODGRZANIE_WODY"], 2)} z&#322;</span></p>
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
                  <p class="c1"><span class="c3">{round(user["KOSZT_STALY_PODGRZANIA"], 2)} z&#322</span></p>
               </td>
               <td class="c7" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">1</span></p>
               </td>
               <td class="c2" colspan="1" rowspan="1">
                  <p class="c1"><span class="c3">{round(user["KOSZT_STALY_PODGRZANIA"] * 1, 2)} z&#322</span></p>
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
                  <p class="c1"><span class="c19 c6">{round(user["KOSZT_STALY_PODGRZANIA"] * 1 + user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_PODGRZANIE_WODY"], 2)} z&#322;</span></p>
               </td>
            </tr>
         </table>
         <p class="c1 c17"><span class="c0"></span></p>
         <a id="t.eb93e17c290906fe80293081e7c6b588eb5cd113"></a><a id="t.2"></a>
         <table class="c18">
            <tr class="c40">
               <td class="c28" colspan="3" rowspan="1">
                  <p class="c1"><span class="c6 c12">Saldo na dzie&#324; {"jakis_dzien"}: [7]+[4] &nbsp; &nbsp; &nbsp; </span><span class="c26 c6">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </span></p>
               </td>
               <td class="c42" colspan="1" rowspan="1">
                  <p class="c30"><span class="c26 c6">&nbsp;</span></p>
               </td>
               <td class="c36" colspan="1" rowspan="1">
                  <p class="c1"><span class="c6 c26">{round(user["KOSZT_STALY_PODGRZANIA"] * 1 + user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_PODGRZANIE_WODY"] + user["ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE"] + user["ZUZYCIE_WODY_CIEPLEJ"] * user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"] + user["STAWKA_ZA_WODE_ZIMNA_I_SCIEKI"] * user["ZUZYCIE_WODY_ZIMNEJ"], 2)} z&#322;</span></p>
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