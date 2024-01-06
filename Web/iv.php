<!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" type="text/css" href="css/util.css">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <link href="css/btn.css" rel="stylesheet" type="text/css" />
    </head>
    <body>
    <?php
        $i = 0;
        $cmd = "cd /var/www/html && python firestore_test.py";
        exec($cmd, $output);
        # $output = $output[0][13] * 10 . '%';
        # print_r($output)
    ?>
        <br><br><br>
        <CENTER>

        <div class="limiter">
            <div class="wrap-table100">
                <div class="table">
                    <div class="row header">

        
        <?php
            $conn = mysqli_connect('localhost', 'root', '11223344', 'Patient');
            if ( !$conn ) die('DB Error');

            $sql1 = "SELECT * FROM patient_info";
            $rs1 = mysqli_query($conn, $sql1);
            
            echo '<div class="cell">환자 번호</div>' .
                '<div class="cell">환자 이름</div>' .
                '<div class="cell">생년월일</div>' .
                '<div class="cell">수액팩 남은 용량</div></div>';

                while($info1 = mysqli_fetch_array($rs1))
                {
                    $split = $output[$i][13] * 10 . '%';
                    #$cmd = "cd /var/www/html && python firestore.py " . $info1['P_ID'];
                    #exec($cmd, $output);
                    
                    #각 열을 하나하나 불러와서 표 만들기
                    echo '<div class="row"><div class="cell" data-title="환자 번호">' . $info1['P_ID'] . '</div>' .
                        '<div class="cell" data-title="환자 이름">' . $info1['P_NAME'] . '</div>' .
                        '<div class="cell" data-title="생년월일">' . $info1['P_BIRTHDATE'] . '</div>' .
                        '<div class="cell" data-title="수액팩 남은 용량">' . $split . '</div></div>';
                    $i++;
                }
                echo '</div></div></div><br><br>';

            mysqli_close($conn);
        ?>
        
        <?php
        /*
            echo '<div class="cell">환자 번호</div>' .
                '<div class="cell">환자 이름</div>' .
                '<div class="cell">생년월일</div>' .
                '<div class="cell">수액팩 남은 용량</div></div>';

            echo '<div class="row"><div class="cell" data-title="환자 번호">' . '0101' . '</div>' .
                '<div class="cell" data-title="환자 이름">' . '홍길동' . '</div>' .
                '<div class="cell" data-title="생년월일">' . '010101' . '</div>' .
                '<div class="cell" data-title="수액팩 남은 용량">' . '0%' . '</div></div>';

            echo '<div class="row"><div class="cell" data-title="환자 번호">' . '1234' . '</div>' .
                '<div class="cell" data-title="환자 이름">' . '엄태현' . '</div>' .
                '<div class="cell" data-title="생년월일">' . '000807' . '</div>' .
                '<div class="cell" data-title="수액팩 남은 용량">' . '40%' . '</div></div>';

            echo '<div class="row"><div class="cell" data-title="환자 번호">' . '1313' . '</div>' .
                '<div class="cell" data-title="환자 이름">' . '신짱구' . '</div>' .
                '<div class="cell" data-title="생년월일">' . '111111' . '</div>' .
                '<div class="cell" data-title="수액팩 남은 용량">' . '70%' . '</div></div>';
            
            echo '<div class="row"><div class="cell" data-title="환자 번호">' . '1414' . '</div>' .
                '<div class="cell" data-title="환자 이름">' . '노진구' . '</div>' .
                '<div class="cell" data-title="생년월일">' . '000101' . '</div>' .
                '<div class="cell" data-title="수액팩 남은 용량">' . $output . '%</div></div>';

            echo '</div></div></div><br><br>';
        */
        ?>

        <div class="btn-container">
            <a href="index.php" class="btn-3d blue">메인페이지로 돌아가기</a>
        </div>
        </CENTER>
    </body>
</html>