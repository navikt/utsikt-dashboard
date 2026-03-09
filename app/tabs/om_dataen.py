import streamlit as st


def om_dataen():
    st.header("Om dataen")
    st.markdown(
        """
        Datagrunnlaget for visualiseringene er hentet fra Oppdragssystemet  og omhandler beregninger.

        En beregning starter som et utbetalingsoppdrag fra fagssystem.  Etterhvert som Oppdragssystemet jobber med beregningen, vil beregningen brytes ned i mindre deler og være innom ulike steg. 


        #### Stoppnivå
        Stoppnivå er et begrep i Oppdragssystemet som brukes for nedbryting av beregninger. En beregning kan brytes ned i f.eks. perioder med tilhørende forfallsdato gjelde forskjellige mottakere eller kan gjelde ulike saker f.eks sykepenger til én bruker men gjelder flere forhold.

        #### Ventestatus
        Ventestatus er  status for stoppnivået,  altså hvor i beregningsløpet et stoppnivå er.  F.eks. et stoppnivå kan ha ventestatusen OVFO (for 'Overført til UR').

        #### Faggruppe
        En faggruppe består av flere fagområder hvor man ønsker en samlet felles skatt-og trekkberegning. F.eks. pensjonsrelaterte ytelser. 

        #### Fagområde
        Fagområde angir selve ytelsen f.eks. arbeidsavklaringspenger. 
        """
    )
