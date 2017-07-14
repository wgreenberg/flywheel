import asyncio

from math import log
from nltk.tokenize import sent_tokenize, word_tokenize
from aiogremlin import DriverRemoteConnection, Graph

GREMLIN_URI = 'ws://localhost:8182/gremlin'

# like SxS, except we don't care about repeat values or order
def cartesian_square(S):
    for i, a in enumerate(S):
        for b in S[i+1:]:
            yield (a, b)

# from section 4.1
def similarity(a, b):
    shared_words = set(word_tokenize(a)) & set(word_tokenize(b))
    return len(shared_words) / (log(len(a)) + log(len(b)))

async def summarize(text, event_loop):
    sentences = sent_tokenize(text)
    remote_connection = await DriverRemoteConnection.open(GREMLIN_URI, 'g')
    g = Graph().traversal().withRemote(remote_connection)

    tx = g
    for i, sentence in enumerate(sentences):
        tx = tx.addV('sentence').as_(str(i)).property('text', sentence)

    for a, b in cartesian_square(range(len(sentences))):
        sent_a = sentences[a]
        sent_b = sentences[b]
        score = similarity(sent_a, sent_b)
        tx = tx.addE('similarity').from_(str(a)).to(str(b)).property('score', score)
        tx = tx.addE('similarity').from_(str(b)).to(str(a)).property('score', score)

    # Block until graph is initialized (is this needed???)
    await tx.next()

    # this is broken af
    print(await g.withComputer().V().pageRank().by(g.V().outE('score')).values('pageRank').toList())

    # Clear out the graph
    await g.V().drop().next()
    await g.E().drop().next()

    # Close our connection
    await remote_connection.close()

    return 'The history of all hitherto existing society is the history of class struggles.'

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    example = '''The history of all hitherto existing society is the history of class struggles.
    
    Freeman and slave, patrician and plebeian, lord and serf, guild-master and journeyman, in a word, oppressor and oppressed, stood in constant opposition to one another, carried on an uninterrupted, now hidden, now open fight, a fight that each time ended, either in a revolutionary reconstitution of society at large, or in the common ruin of the contending classes.
    
    In the earlier epochs of history, we find almost everywhere a complicated arrangement of society into various orders, a manifold gradation of social rank. In ancient Rome we have patricians, knights, plebeians, slaves; in the Middle Ages, feudal lords, vassals, guild-masters, journeymen, apprentices, serfs; in almost all of these classes, again, subordinate gradations.
    
    The modern bourgeois society that has sprouted from the ruins of feudal society has not done away with class antagonisms. It has but established new classes, new conditions of oppression, new forms of struggle in place of the old ones. '''
    print(loop.run_until_complete(summarize(example, loop)))
