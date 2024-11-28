import unittest

class ContextTest(unittest.TestCase):

    pattern_song = Pattern("fifty_song.png").similar(0.76)
    pattern_correct = Pattern("correct_btn.png").similar(0.94)

    def setUp(self):
        click("main_view.png")
        click(Pattern("fifty_words_btn.png").similar(0.94)) # 開啟五十音介面
        wait(Pattern("fifty_view.png").similar(0.93))
    
    def test_fifity_words(self):
        try:
            fifty_words_btn = ["a.png","i.png","u.png","e.png","o.png","ka.png","ki.png","ku.png","ke.png","ko.png","sa.png","shi.png","su.png","se.png","so.png","ta.png","chi.png","tsu.png","te.png","to.png","na.png","ni.png","nu.png","ne.png","no.png","ha.png","hi.png","fu.png","he.png","ho.png","ma.png","mi.png","mu.png","me.png","mo.png","ya.png","yu.png","yo.png","ra.png","ri.png","ru.png","re.png","ro.png","wa.png","wo.png","n.png"]
            for i in fifty_words_btn:
                pattern_fifty_words = Pattern(i).similar(0.7)
                click(pattern_fifty_words)
                assert exists(self.pattern_correct) # 檢查五十音按鈕顏色是否有變化
        except Exception as e:
            print(e)
    
    def test_song(self):
        try:
            click(self.pattern_song)
            assert exists(self.pattern_correct) # 檢查歌曲按鈕顏色是否有變化
            wait(2)
            click(self.pattern_song)
            assert not exists(self.pattern_correct) # 檢查回復歌曲按鈕原來顏色
            click(self.pattern_song)
            wait(2)
            type(Key.ESC)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ContextTest)
    unittest.TextTestRunner(verbosity=2).run(suite)    
